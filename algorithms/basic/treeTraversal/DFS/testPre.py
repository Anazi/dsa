import unittest
from unittest.mock import Mock
from unittest.mock import patch

from DFS_PreOrder import BinarySearchTree


class PreTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(PreTests, self).__init__(*args, **kwargs)

    def test_pre_order(self):

        test_values = [47, 21, 76, 82, 52, 18, 27]

        bst = BinarySearchTree()
        for i in test_values:
            bst.insert(i)

        expected_res = [47, 21, 18, 27, 76, 52, 82]

        actual_res = bst.dfs_pre_order()

        self.assertEqual(actual_res, expected_res, 'correctly traversed')

