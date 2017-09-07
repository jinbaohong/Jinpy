import unittest
from classTry import Animal

class TestAnimal(unittest.TestCase):
    def setUp(self):
        self.Shian = Animal('ShianGan','100')
    def tearDown(self):
        self.Shian = None
    def test_age(self):
        #Shian = Animal('ShianGan', '100')
        self.assertEqual(self.Shian.getAge(), 101)

    def test_name(self):
        #Shian = Animal('ShianGan', '100')
        self.assertEqual(self.Shian.getName(), 'ShianGan')

if __name__ == '__main__':
    unittest.main()

