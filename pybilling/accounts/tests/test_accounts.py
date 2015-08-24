from django.test import TestCase

from accounts.models import UserAccount, PersonalDataPerson


class UserAccountTest(TestCase):
    def test_create_account(self):
        user, created = UserAccount.objects.get_or_create(name='Dmitry')
        user.refresh_from_db()

        self.assertTrue(created)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, 'Dmitry')
        self.assertEqual(user.balance, 0)
        self.assertEqual(user.bonus_balance, 0)
        self.assertEqual(user.bonus_balance, 0)
        self.assertEqual(user.language, 'ru')

    def test_create_personal_data(self):
        user, created = UserAccount.objects.get_or_create(name='Dmitry')

        pers_data = user.add_personal_data(PersonalDataPerson,
                                           fio='Dmitry Shilyaev',
                                           birth='1983-09-05')

        print 'fio: %s' % pers_data.fio_lat
