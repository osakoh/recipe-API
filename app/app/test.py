from django.test import TestCase

from app.calc import add


class CalcTestCase(TestCase):
    def test_add_numbers(self):
        """Test adding numbers"""
        expected = 11
        actual = add(3, 8)
        self.assertEqual(expected, actual)


#  docker-compose run app sh -c "python manage.py test"
