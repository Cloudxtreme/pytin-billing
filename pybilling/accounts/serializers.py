from __future__ import unicode_literals

from rest_framework import serializers
from django.apps import apps

from accounts.models import UserAccount, UserContact, PersonalData


class PersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalData

    def update(self, instance, validated_data):
        account = instance.account

        extra_data_class_name = validated_data.get('type', instance.type)
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
        # fetch extended data fields
        details = instance.extended
        personal_data = {}
        for field in details._meta.fields:
            if field.is_relation:
                continue

            personal_data[field.name] = unicode(getattr(details, field.name))

        # fetch common data fields
        common_data = super(PersonalDataSerializer, self).to_representation(instance)
        for field_name in common_data:
            personal_data[field_name] = common_data[field_name]

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

    def create(self, validated_data):
        if 'pk' in self.initial_data:
            validated_data['id'] = self.initial_data['pk']

        return super(UserAccountSerializer, self).create(validated_data)
