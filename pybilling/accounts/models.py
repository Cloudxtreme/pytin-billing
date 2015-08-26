from __future__ import unicode_literals

import re

import pytils
from django.core.validators import validate_email, RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Custom model fields validators
validate_phone = RegexValidator(
    re.compile(r'^\+\d+\s+\d{3}\s+\d+\Z'),
    _("Phone format is +#[#] ### #######"),
    'invalid'
)


def populate_fields(obj, **kwargs):
    assert obj

    for field_name in kwargs:
        if hasattr(obj, field_name):
            setattr(obj, field_name, kwargs[field_name])

    return obj


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
    language = models.CharField(db_index=True, default='ru', max_length=15)
    balance = models.IntegerField(db_index=True, default=0, null=False)
    bonus_balance = models.IntegerField(db_index=True, default=0, null=False)

    def update_contact(self, name, type, address, default=False, verified=False, validator=None):
        """
        Updates or crates user contact.

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

        user_contact, created = UserContact.objects.get_or_create(
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

    def update_personal_data(self, klass, **kwargs):
        """
        Updates the personal data of specific klass.

        :param klass: Type of the personal data, such as PersonalDataEntrepreneur
        :param kwargs: Personal data parameters, based on klass
        :return: Created personal data object of type klass
        """
        assert klass

        return PersonalData.update_personal_data(self, klass, **kwargs)


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
    account = models.ForeignKey(UserAccount)

    type = models.CharField(max_length=55, db_index=True, null=False)
    default = models.BooleanField(null=False, db_index=True, default=False)
    verified = models.BooleanField(null=False, db_index=True, default=False)

    @staticmethod
    def update_personal_data(account, data_klass, **kwargs):
        """
        Create personal data based on data_klass extension classes. There are number of predefined classes,
        but you can safely add custom private data classes with OneToOneField to PersonalData.
        There is only ONE personal data of type klass is allowed per user.
        :param data_klass:
        :param kwargs:
        :return:
        """
        assert account
        assert data_klass

        common_data, created = PersonalData.objects.get_or_create(
            type=data_klass.__name__,
            account=account,
        )

        common_data = populate_fields(common_data, **kwargs)

        common_data.full_clean()
        common_data.save()

        personal_data, created = data_klass.objects.get_or_create(
            common_data=common_data,
            defaults=kwargs
        )

        personal_data.full_clean()
        personal_data.save()

        return personal_data


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

    def clean(self):
        if not self.fio_lat:
            self.fio_lat = pytils.translit.translify(self.fio)


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

    def clean(self):
        if not self.fio_lat:
            self.fio_lat = pytils.translit.translify(self.fio)


class PersonalDataCompany(models.Model):
    common_data = models.OneToOneField(PersonalData, primary_key=True)

    company_name = models.CharField(max_length=255, db_index=True)
    company_name_lat = models.CharField(blank=True, max_length=255, db_index=True)
    inn = models.CharField(max_length=55, db_index=True)
    ogrn = models.CharField(max_length=55, db_index=True, null=True)
    kpp = models.CharField(max_length=55, db_index=True)

    postal_person = models.CharField(max_length=255, db_index=True)
    postal_address = models.CharField(max_length=255, db_index=True)
    postal_index = models.CharField(max_length=35, db_index=True)
    company_address = models.CharField(max_length=255, db_index=True)

    phone = models.CharField(blank=False, db_index=True, max_length=55, validators=[validate_phone])
    email = models.CharField(blank=False, db_index=True, max_length=55, validators=[validate_email])

    def clean(self):
        if not self.company_name:
            self.company_name_lat = pytils.translit.translify(self.company_name)


class PersonalDataForeignPerson(models.Model):
    common_data = models.OneToOneField(PersonalData, primary_key=True)

    country = models.CharField(max_length=55, db_index=True)
    fio_lat = models.CharField(max_length=255, db_index=True)
    passport = models.CharField(max_length=255, db_index=True)
    birth = models.DateTimeField(null=False, db_index=True)
    postal_address = models.CharField(max_length=255, db_index=True)
    phone = models.CharField(blank=False, db_index=True, max_length=55, validators=[validate_phone])
    email = models.CharField(blank=False, db_index=True, max_length=55, validators=[validate_email])


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


class PersonalDataForeignCompany(models.Model):
    common_data = models.OneToOneField(PersonalData, primary_key=True)

    country = models.CharField(max_length=55, db_index=True)
    company_name_lat = models.CharField(max_length=255, db_index=True)

    postal_address = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)

    phone = models.CharField(blank=False, db_index=True, max_length=55, validators=[validate_phone])
    email = models.CharField(blank=False, db_index=True, max_length=55, validators=[validate_email])
