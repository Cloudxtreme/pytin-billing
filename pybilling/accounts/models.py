from __future__ import unicode_literals

import re

import pytils
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, RegexValidator
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Custom model fields validators
validate_phone = RegexValidator(
        re.compile(r'^\+\d+\s+\d{3}\s+\d+\Z'),
        _("Phone format is +#[#] ### #######"),
        'invalid'
)


def get_supported_fields(klass, **kwargs):
    """
    Fill the obj fields based on kwargs.

    :param klass: Object class to check for fields.
    :param kwargs: key=value parameters.
    :return: Filled object.
    """
    assert klass

    supported_fields = {}
    for field_name in kwargs:
        if ModelFieldChecker.is_model_field(klass, field_name):
            supported_fields[field_name] = kwargs[field_name]

    return supported_fields


class ModelFieldChecker:
    """
    Utility class to query Django model fields.
    """
    builtin = ['pk']

    def __init__(self):
        pass

    @staticmethod
    def is_field_or_property(object, name):
        """
        Check if field name belongs to model fields or properties
        """
        assert name is not None, "Parameter 'name' must be defined."
        assert issubclass(object.__class__, models.Model), "Class 'class_type' must be the subclass of models.Model."

        return ModelFieldChecker.is_model_field(object.__class__, name) or hasattr(object, name)

    @staticmethod
    def is_model_field(class_type, name):
        """
        Check if field name belongs to model fields
        """
        assert name is not None, "Parameter 'name' must be defined."
        assert issubclass(class_type, models.Model), "Class 'class_type' must be the subclass of models.Model."

        if name in ModelFieldChecker.builtin:
            return True

        try:
            return name in [f.name for f in class_type._meta.fields]
        except models.FieldDoesNotExist:
            return False

    @staticmethod
    def get_field_value(resource, field_name, default=''):
        if ModelFieldChecker.is_model_field(resource.__class__, field_name):
            return getattr(resource, field_name, default)
        else:
            return resource.get_option_value(field_name, default=default)


class ManagedQuerySet(QuerySet):
    """
    This query set is able to search in related specific PersonalData object.
    If field is not PersonalData model field, then the lookup query to related specific
    personal data object is added.
    """

    def filter(self, *args, **kwargs):
        """
        search_fields keys can be specified with lookups:
        https://docs.djangoproject.com/en/1.7/ref/models/querysets/#field-lookups
        """
        search_fields = kwargs

        query = {}

        for field_name_with_lookup in search_fields.keys():
            field_name = field_name_with_lookup.split('__')[0]

            if ModelFieldChecker.is_model_field(PersonalData, field_name):
                query[field_name_with_lookup] = search_fields[field_name_with_lookup]
            else:
                if 'type' not in search_fields:
                    raise ValidationError(
                            {'type': _("Field 'type' must be defined to be able to search by extended data.")})

                lookup_table_name = search_fields['type'].lower()
                lookup_field = "%s__%s" % (lookup_table_name, field_name_with_lookup)

                query[lookup_field] = search_fields[field_name_with_lookup]

        return super(ManagedQuerySet, self).filter(*args, **query).distinct()


class PersonalDataObjectManager(models.Manager):
    """
    Query manager with support for query by options.
    """

    def get_queryset(self):
        return ManagedQuerySet(self.model)


class UserAccount(models.Model):
    """
    User model for the account.
    """

    KNOWN_VALIDATORS = {
        'email': validate_email,
        'phone': validate_phone
    }

    name = models.CharField(db_index=True, max_length=155, null=False)
    created_at = models.DateTimeField(db_index=True, default=timezone.now, null=False)
    last_login_at = models.DateTimeField(db_index=True, null=True)
    language = models.CharField(db_index=True, default='RU', max_length=15)
    balance = models.IntegerField(db_index=True, default=0, null=False)
    bonus_balance = models.IntegerField(db_index=True, default=0, null=False)

    def __unicode__(self):
        return "u%s" % self.id

    def update_contact(self, name, type, address, default=False, verified=False, validator=None):
        """
        Updates or crates user contact. If there is a contact with the same address value, it's being
        updated, created - otherwise.

        :param name: Arbitrary name of the contact, such as home or main.
        :param type: Type of the contact. Such as email or skype.
        :param address: Contact address in the specific contact type (ICQ number, phone number, etc).
        :param default: True if this contact is default.
        :param verified: True if this contact was verified.
        :param validator: You can pass any model field validator.
        :return: Created or updated user contact.
        """
        assert name
        assert type
        assert address

        name = name.strip()
        type = type.strip().lower()
        address = address.strip()

        if not validator:
            if type in UserAccount.KNOWN_VALIDATORS:
                validator = UserAccount.KNOWN_VALIDATORS[type]

        if validator:
            validator(address)

        user_contact, created = UserContact.objects.update_or_create(
                account=self,
                address=address,
                defaults=dict(
                        name=name,
                        type=type,
                        default=default,
                        verified=verified
                )
        )

        return user_contact

    def add_personal_data(self, data_class, **kwargs):
        """
        Add personal data of type 'data_klass' to the account.
        :returns Object of type PersonalData with related object of 'data_klass' type.
        """
        assert data_class

        if 'data_class' in kwargs:
            del kwargs['data_class']

        kwargs['account'] = self
        kwargs['type'] = data_class.__name__

        pdata = get_supported_fields(PersonalData, **kwargs)
        common_data = PersonalData(
                **pdata
        )

        common_data.full_clean()
        common_data.save()

        try:
            personal_data, created = data_class.objects.update_or_create(
                    common_data=common_data,
                    defaults=get_supported_fields(data_class, **kwargs)
            )

            personal_data.full_clean()
            personal_data.save()
        except Exception:
            common_data.delete()
            raise

        return personal_data.common_data


class UserContact(models.Model):
    """
    User contact, such as Skype, Email, ICQ, etc.
    """
    account = models.ForeignKey(UserAccount)

    name = models.CharField(db_index=True, max_length=255)
    address = models.CharField(db_index=True, max_length=255)
    type = models.CharField(db_index=True, max_length=15)
    default = models.BooleanField(db_index=True, default=False, null=False)
    verified = models.BooleanField(db_index=True, default=False, null=False)


class PersonalData(models.Model):
    """
    Model to control User personal info, such as forms for domain registration
    and company requisites.
    """
    objects = PersonalDataObjectManager()

    account = models.ForeignKey(UserAccount)

    type = models.CharField(max_length=55, db_index=True, null=False)
    default = models.BooleanField(null=False, db_index=True, default=False)
    verified = models.BooleanField(null=False, db_index=True, default=False)

    def __unicode__(self):
        return "%s (%s, %s, %s)" % (self.id, self.type, self.default, self.verified)

    def __getattr__(self, attrname):
        """
        Override getters to allow access to extended fields via root PersonalData.
        pd = PersonalData(fields...)
        pd_ext = PersonalDataPerson(fields..)
        pd_ext.common_data = pd
        pd_ext.save()

        # This calls are the same
        print pd.fio
        print pd.extended.fio

        print pd.type  # called from pd itself, because it is a model field.
        """
        assert attrname

        if not ModelFieldChecker.is_model_field(PersonalData, attrname):
            return getattr(self.extended, attrname)

        return super(PersonalData, self).__getattr__(attrname)

    def update(self, **kwargs):
        if 'account' in kwargs:
            del kwargs['account']

        fields_map = get_supported_fields(PersonalData, **kwargs)
        for field_name in fields_map:
            setattr(self, field_name, fields_map[field_name])

        self.full_clean()
        self.save()

        extra_data = self.extended
        if extra_data:
            fields_map = get_supported_fields(extra_data.__class__, **kwargs)
            for field_name in fields_map:
                setattr(extra_data, field_name, fields_map[field_name])

            extra_data.full_clean()
            extra_data.save()

        return self

    @property
    def extended(self):
        """
        Getting extended personal data info.

        :return: Personal data object based on 'type' field.
        """
        attribute_name = self.type.lower()
        if hasattr(self, attribute_name):
            return getattr(self, attribute_name)

        return None


class PersonalDataPerson(models.Model):
    common_data = models.OneToOneField(PersonalData, primary_key=True)

    fio = models.CharField(blank=False, db_index=True, max_length=255)
    fio_lat = models.CharField(blank=True, db_index=True, max_length=255)
    passport = models.CharField(blank=False, max_length=555)
    birth = models.DateTimeField(blank=False, db_index=True)
    postal_address = models.CharField(blank=False, db_index=True, max_length=255)
    postal_index = models.CharField(blank=False, db_index=True, max_length=35)
    phone = models.CharField(blank=False, db_index=True, max_length=55, validators=[validate_phone])
    email = models.CharField(blank=False, db_index=True, max_length=55, validators=[validate_email])

    def __unicode__(self):
        return self.fio

    def clean(self):
        if not self.fio_lat:
            self.fio_lat = pytils.translit.translify(self.fio, strict=False)
        else:
            self.fio_lat = pytils.translit.translify(self.fio_lat, strict=False)


class PersonalDataEntrepreneur(models.Model):
    common_data = models.OneToOneField(PersonalData, primary_key=True)

    fio = models.CharField(max_length=255, db_index=True)
    fio_lat = models.CharField(blank=True, max_length=255, db_index=True)
    passport = models.CharField(max_length=555)
    inn_code = models.CharField(max_length=55, db_index=True)
    birth = models.DateTimeField(null=False, db_index=True)
    postal_address = models.CharField(max_length=255, db_index=True)
    postal_index = models.CharField(max_length=35, db_index=True)
    phone = models.CharField(blank=False, db_index=True, max_length=55, validators=[validate_phone])
    email = models.CharField(blank=False, db_index=True, max_length=55, validators=[validate_email])

    def __unicode__(self):
        return "%s (%s)" % (self.fio, self.inn_code)

    def clean(self):
        if not self.fio_lat:
            self.fio_lat = pytils.translit.translify(self.fio, strict=False)
        else:
            self.fio_lat = pytils.translit.translify(self.fio_lat, strict=False)


class PersonalDataCompany(models.Model):
    common_data = models.OneToOneField(PersonalData, primary_key=True)

    company_name = models.CharField(max_length=255, db_index=True)
    company_name_lat = models.CharField(blank=True, max_length=255, db_index=True)
    inn = models.CharField(max_length=10, db_index=True)
    ogrn = models.CharField(max_length=13, db_index=True, null=True)
    kpp = models.CharField(max_length=9, db_index=True)

    postal_person = models.CharField(max_length=255, db_index=True)
    postal_address = models.CharField(max_length=255, db_index=True)
    postal_index = models.CharField(max_length=35, db_index=True)
    company_address = models.CharField(max_length=255, db_index=True)

    phone = models.CharField(blank=False, db_index=True, max_length=55, validators=[validate_phone])
    email = models.CharField(blank=False, db_index=True, max_length=55, validators=[validate_email])

    def __unicode__(self):
        return self.company_name

    def clean(self):
        if not self.company_name_lat:
            self.company_name_lat = pytils.translit.translify(self.company_name, strict=False)
        else:
            self.company_name_lat = pytils.translit.translify(self.company_name_lat, strict=False)


class PersonalDataForeignPerson(models.Model):
    common_data = models.OneToOneField(PersonalData, primary_key=True)

    country = models.CharField(max_length=55, db_index=True)
    fio_lat = models.CharField(max_length=255, db_index=True)
    passport = models.CharField(max_length=255, db_index=True)
    birth = models.DateTimeField(null=False, db_index=True)
    postal_address = models.CharField(max_length=255, db_index=True)
    phone = models.CharField(blank=False, db_index=True, max_length=55, validators=[validate_phone])
    email = models.CharField(blank=False, db_index=True, max_length=55, validators=[validate_email])

    def __unicode__(self):
        return self.fio_lat

    def clean(self):
        self.fio_lat = pytils.translit.translify(self.fio_lat, strict=False)


class PersonalDataForeignEntrepreneur(models.Model):
    common_data = models.OneToOneField(PersonalData, primary_key=True)

    country = models.CharField(max_length=55, db_index=True)
    fio_lat = models.CharField(max_length=255, db_index=True)
    passport = models.CharField(max_length=255, db_index=True)
    inn_code = models.CharField(max_length=55, db_index=True)
    birth = models.DateTimeField(null=False, db_index=True)
    postal_address = models.CharField(max_length=255, db_index=True)
    phone = models.CharField(blank=False, db_index=True, max_length=55, validators=[validate_phone])
    email = models.CharField(blank=False, db_index=True, max_length=55, validators=[validate_email])

    def __unicode__(self):
        return "%s (%s)" % (self.fio_lat, self.inn_code)

    def clean(self):
        self.fio_lat = pytils.translit.translify(self.fio_lat, strict=False)


class PersonalDataForeignCompany(models.Model):
    common_data = models.OneToOneField(PersonalData, primary_key=True)

    country = models.CharField(max_length=55, db_index=True)
    company_name_lat = models.CharField(max_length=255, db_index=True)

    postal_address = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)

    phone = models.CharField(blank=False, db_index=True, max_length=55, validators=[validate_phone])
    email = models.CharField(blank=False, db_index=True, max_length=55, validators=[validate_email])

    def __unicode__(self):
        return self.company_name_lat

    def clean(self):
        self.company_name_lat = pytils.translit.translify(self.company_name_lat, strict=False)
