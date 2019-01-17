from main import check_api_for_password

import unittest
import yaml


class TestMethods(unittest.TestCase):
    def test_API(self):
        with open("example_config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
            test_pw_fail = cfg['test_password_fail']
            test_pw_pass = cfg['test_password_pass']

        self.assertGreater(check_api_for_password(test_pw_fail),0)
        self.assertEqual(check_api_for_password(test_pw_pass),-1)

if __name__ == '__main__':
    unittest.main()