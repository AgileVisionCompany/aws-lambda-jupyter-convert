
import unittest
from handler import execute_notebook

class TestExecution(unittest.TestCase):

    def test_upper(self):
        with open('sample.ipynb', 'r') as source:
            result = execute_notebook(source)

        self.assertIsNotNone(result)
        print(result)

if __name__ == '__main__':
    unittest.main()
