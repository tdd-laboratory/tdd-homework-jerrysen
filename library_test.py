import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    def test_iso8601_date(self):
        self.assert_extract('I was born on 2015-07-25.', library.dates_iso8601, '2015-07-25')

    def test_dates_fmt2(self):
        self.assert_extract('I was born on 25 Jan 2017.', library.dates_fmt2, '25 Jan 2017')

    def test_iso8601_date_valid_timestamp_T_hour_minute(self):
        self.assert_extract("This is a valid timestamp 2012-01-12T03:00.", library.dates_iso8601, '2012-01-12T03:00')

    def test_iso8601_date_valid_timestamp_space_hour_minute(self):
        self.assert_extract("This is valid with space 2012-01-12 03:00.", library.dates_iso8601, '2012-01-12 03:00')

    def test_iso8601_date_valid_timestamp_T_hour_minute_second(self):
        self.assert_extract("This is a valid timestamp 2012-01-12T03:00:25.", library.dates_iso8601, '2012-01-12T03:00:25')

    def test_iso8601_date_valid_timestamp_space_hour_minute_second(self):
        self.assert_extract("This is a valid timestamp 2012-01-12 03:00:25.", library.dates_iso8601, '2012-01-12 03:00:25')

    def test_iso8601_date_valid_timestamp_T_hour_minute_second_millisecond(self):
        self.assert_extract("This is a valid timestamp 2012-01-12T03:00:25.033.", library.dates_iso8601, '2012-01-12T03:00:25.033')

    def test_iso8601_date_valid_timestamp_space_hour_minute_second_millisecond(self):
        self.assert_extract("This is a valid timestamp 2012-01-12 03:00:25.033.", library.dates_iso8601, '2012-01-12 03:00:25.033')

    def test_iso8601_date_invalid_timestamp_T__hour_minute(self):
        self.assert_extract("This is a invalid timestamp 2012.01.12T03:00.", library.dates_iso8601, '2012-01-12T03:00')

    def test_iso8601_date_invalid_date(self):
        self.assert_extract("This is a invalid timestamp 2012/01/12.", library.dates_iso8601, '2012-01-12')


if __name__ == '__main__':
    unittest.main()
