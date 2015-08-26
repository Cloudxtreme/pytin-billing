from rest_framework import serializers

from accounts.models import UserAccount, UserContact


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
    contacts = UserContactSerializer(source='usercontact_set', many=True, read_only=True)

    class Meta:
        model = UserAccount
