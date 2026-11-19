import unittest
from logic import calculate_average, validate_grade, get_status


class TestJournalLogic(unittest.TestCase):
    def test_calculate_average(self):
        self.assertEqual(calculate_average("10, 9, 8, 9"), 9.0)
        self.assertEqual(calculate_average(""), 0.0)

    def test_validate_grade(self):
        self.assertTrue(validate_grade("10"))
        self.assertTrue(validate_grade("1"))
        self.assertFalse(validate_grade("11"))
        self.assertFalse(validate_grade("abc"))

    def test_get_status(self):
        self.assertEqual(get_status(9.2), "Отлично (5)")
        self.assertEqual(get_status(7.5), "Хорошо (4)")
        self.assertEqual(get_status(5.0), "Удовл. (3)")
        self.assertEqual(get_status(3.2), "Неуспевающий (2)")


if __name__ == "__main__":
    unittest.main()
    