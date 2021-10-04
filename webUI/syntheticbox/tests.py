from django.test import TestCase
import pandas as pd
from .models import join_files
from pandas._testing import assert_frame_equal


class JoinFilesTestCase(TestCase):

    def test_two_files_can_be_joined(self):
        csv1 = pd.DataFrame(data={'user_id': [1, 2], 'age': [43, 28]})
        csv2 = pd.DataFrame(data={'user_id': [1, 2], 'gender': ['F', 'M']})
        csv_files = [csv1, csv2]
        joined_file = join_files(csv_files, 'user_id')

        expected = pd.DataFrame(data={'user_id': [1, 2], 'age': [43, 28], 'gender': ['F', 'M']})
        assert_frame_equal(joined_file, expected)

    def test_three_files_can_be_joined(self):
        csv1 = pd.DataFrame(data={'user_id': [1, 2], 'age': [43, 28]})
        csv2 = pd.DataFrame(data={'user_id': [1, 2], 'gender': ['F', 'M']})
        csv3 = pd.DataFrame(data={'user_id': [1, 2], 'name': ['A', 'B']})
        csv_files = [csv1, csv2, csv3]
        joined_file = join_files(csv_files, 'user_id')

        expected = pd.DataFrame(data={'user_id': [1, 2], 'age': [43, 28], 'gender': ['F', 'M'], 'name': ['A', 'B']})
        assert_frame_equal(joined_file, expected)

    def test_join_files_works_when_different_order(self):
        csv1 = pd.DataFrame(data={'user_id': [1, 2], 'age': [43, 28]})
        csv2 = pd.DataFrame(data={'user_id': [2, 1], 'gender': ['M', 'F']})
        csv_files = [csv1, csv2]
        joined_file = join_files(csv_files, 'user_id')

        expected = pd.DataFrame(data={'user_id': [1, 2], 'age': [43, 28], 'gender': ['F', 'M']})
        assert_frame_equal(joined_file, expected)

    def test_join_files_works_when_multiple_of_same_column(self):
        csv1 = pd.DataFrame(data={'user_id': [1, 1, 2, 2], 'purchase_amount': [32, 12, 11, 734]})
        csv2 = pd.DataFrame(data={'user_id': [1, 2], 'gender': ['F', 'M']})
        csv_files = [csv1, csv2]
        joined_file = join_files(csv_files, 'user_id')

        expected = pd.DataFrame(
            data={'user_id': [1, 1, 2, 2], 'purchase_amount': [32, 12, 11, 734], 'gender': ['F', 'F', 'M', 'M']})
        assert_frame_equal(joined_file, expected)

    def test_join_files_drops_row_if_no_match(self):
        csv1 = pd.DataFrame(data={'user_id': [1, 2], 'age': [43, 28]})
        csv2 = pd.DataFrame(data={'user_id': [2], 'gender': ['M']})
        csv_files = [csv1, csv2]
        joined_file = join_files(csv_files, 'user_id')

        expected = pd.DataFrame(data={'user_id': [2], 'age': [28], 'gender': ['M']})
        assert_frame_equal(joined_file, expected)
