import unittest

import requests


class MyTestCase(unittest.TestCase):
    def test_something(self):
        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'
        }
        res = requests.get(url='https://baidu.com', headers=headers).content
        print(res)
        flag = False
        if res:
            flag = True
        self.assertEqual(True, flag)


if __name__ == '__main__':
    unittest.main()
