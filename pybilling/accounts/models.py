from django.db import models
from django.utils import timezone


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
    name = models.CharField(db_index=True, max_length=155, null=False)
    created_at = models.DateTimeField(db_index=True, default=timezone.now, null=False)
    last_login_at = models.DateTimeField(db_index=True, null=True)
    language = models.CharField(db_index=True, default='ru', max_length=15)
    balance = models.IntegerField(db_index=True, default=0, null=False)
    bonus_balance = models.IntegerField(db_index=True, default=0, null=False)

    def add_personal_data(self, klass, **kwargs):
        assert klass

        return PersonalData.create_personal_data(self, klass, **kwargs)


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
    def create_personal_data(account, data_klass, **kwargs):
        """
        Create personal data based on data_klass extension classes. There are number of predefined classes,
        but you can safely add custom private data classes with OneToOneField to PersonalData.
        :param data_klass:
        :param kwargs:
        :return:
        """
        assert account
        assert data_klass

        common_data = populate_fields(PersonalData(), **kwargs)
        common_data.account = account
        common_data.type = data_klass.__name__
        common_data.save()

        personal_data = data_klass()
        personal_data = populate_fields(personal_data, **kwargs)
        personal_data.common_data = common_data
        personal_data.save()

        return personal_data


class PersonalDataPerson(models.Model):
    common_data = models.OneToOneField(PersonalData, primary_key=True)

    fio = models.CharField(blank=False, db_index=True, max_length=355)
    fio_lat = models.CharField(blank=False, db_index=True, max_length=355, null=False)
    passport = models.CharField(blank=False, max_length=555)
    birth = models.DateTimeField(blank=False, db_index=True)
    postal_address = models.CharField(blank=False, db_index=True, max_length=355)
    postal_index = models.CharField(blank=False, db_index=True, max_length=35)
    phone = models.CharField(blank=False, db_index=True, max_length=55)
    email = models.CharField(blank=False, db_index=True, max_length=55)


class PersonalDataEntrepreneur(models.Model):
    common_data = models.OneToOneField(PersonalData, primary_key=True)

    fio = models.CharField(max_length=355, db_index=True)
    fio_lat = models.CharField(max_length=355, db_index=True)
    passport = models.CharField(max_length=555)
    inn_code = models.CharField(max_length=55, db_index=True)
    birth = models.DateTimeField(null=False, db_index=True)
    postal_address = models.CharField(max_length=355, db_index=True)
    postal_index = models.CharField(max_length=35, db_index=True)
    phone = models.CharField(max_length=55, db_index=True)
    email = models.CharField(max_length=55, db_index=True)


class PersonalDataCompany(models.Model):
    common_data = models.OneToOneField(PersonalData, primary_key=True)

    company_name = models.CharField(max_length=355, db_index=True)
    company_name_lat = models.CharField(max_length=555)
    inn = models.CharField(max_length=55, db_index=True)
    ogrn = models.CharField(max_length=55, db_index=True, null=True)
    kpp = models.CharField(max_length=55, db_index=True)

    postal_person = models.CharField(max_length=355, db_index=True)
    postal_address = models.CharField(max_length=355, db_index=True)
    postal_index = models.CharField(max_length=35, db_index=True)
    company_address = models.CharField(max_length=355, db_index=True)

    phone = models.CharField(max_length=55, db_index=True)
    email = models.CharField(max_length=55, db_index=True)


class PersonalDataForeignPerson(models.Model):
    common_data = models.OneToOneField(PersonalData, primary_key=True)

    country = models.CharField(max_length=55, db_index=True)
    fio_lat = models.CharField(max_length=355, db_index=True)
    passport = models.CharField(max_length=555)
    birth = models.DateTimeField(null=False, db_index=True)
    postal_address = models.CharField(max_length=355, db_index=True)
    phone = models.CharField(max_length=55, db_index=True)
    email = models.CharField(max_length=55, db_index=True)


class PersonalDataForeignEntrepreneur(models.Model):
    common_data = models.OneToOneField(PersonalData, primary_key=True)

    country = models.CharField(max_length=55, db_index=True)
    fio_lat = models.CharField(max_length=355, db_index=True)
    passport = models.CharField(max_length=555)
    inn_code = models.CharField(max_length=55, db_index=True)
    birth = models.DateTimeField(null=False, db_index=True)
    postal_address = models.CharField(max_length=355, db_index=True)
    phone = models.CharField(max_length=55, db_index=True)
    email = models.CharField(max_length=55, db_index=True)


class PersonalDataForeignCompany(models.Model):
    common_data = models.OneToOneField(PersonalData, primary_key=True)

    country = models.CharField(max_length=55, db_index=True)
    company_name_lat = models.CharField(max_length=355, db_index=True)

    postal_address = models.CharField(max_length=355)
    company_address = models.CharField(max_length=355)

    phone = models.CharField(max_length=55, db_index=True)
    email = models.CharField(max_length=55, db_index=True)
