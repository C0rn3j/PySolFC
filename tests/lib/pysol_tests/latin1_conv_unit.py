# Written by Shlomi Fish, under the MIT Expat License.

import unittest

from pysollib.mfxutil import latin1_normalize


class MyTests(unittest.TestCase):
    def test_output(self):
        self.assertEqual(latin1_normalize('HELLO%%good'), 'hellogood')
