from __future__ import unicode_literals

from rest_framework import serializers
from django.apps import apps

from accounts.models import UserAccount, UserContact, PersonalData


class PersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalData

    def update(self, instance, validated_data):
        account = instance.account

        extra_data_class_name = validated_data.get('type')
        extra_data_class = apps.get_model('accounts', extra_data_class_name)

        if extra_data_class_name != instance.type:
            instance.delete()
            instance = account.add_personal_data(extra_data_class, **self.initial_data)
        else:
            instance.update(**self.initial_data)
            instance.refresh_from_db()

        return instance

    def create(self, validated_data):
        account = validated_data.get('account')

        extra_data_class_name = validated_data.get('type')
        extra_data_class = apps.get_model('accounts', extra_data_class_name)

        instance = account.add_personal_data(extra_data_class, **self.initial_data)

        return instance

    def to_representation(self, instance):
        """
        Merge fields from PersonalData and specific extra data object.
        :param instance:
        :return:
        """
        details = instance.extended

        personal_data = {}
        if details:
            for field in details._meta.fields:
                if field.is_relation:
                    continue

                personal_data[field.name] = unicode(getattr(details, field.name))

        for field in instance._meta.fields:
            if field.is_relation:
                continue

            personal_data[field.name] = unicode(getattr(instance, field.name))

        personal_data['id'] = instance.pk

        return personal_data


class UserContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContact

    def create(self, validated_data):
        user_account = validated_data.get('account')

        user_contact = user_account.update_contact(
            name=validated_data.get('name'),
            type=validated_data.get('type'),
            address=validated_data.get('address'),
            default=validated_data.get('default', False),
            verified=validated_data.get('verified', False),
        )

        return user_contact


class UserAccountSerializer(serializers.ModelSerializer):
    contacts = UserContactSerializer(source='usercontact_set', many=True, read_only=True, required=False)
    personal_data = PersonalDataSerializer(source='personaldata_set', many=True, read_only=True, required=False)

    class Meta:
        model = UserAccount
        read_only_fields = ('balance', 'bonus_balance', 'created_at', 'last_login_at', 'personal_data', 'contacts')
