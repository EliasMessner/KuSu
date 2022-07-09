from unittest import TestCase
from statistics import *


class Test(TestCase):
    def test_remove_all_tags(self):
        self.assertEqual(remove_all_tags("example_xml.xml"),
                         "\n\nTove\n"
                         "Jani\n"
                         "Reminder\n"
                         "Don't forget me this weekend!\n"
                         )
