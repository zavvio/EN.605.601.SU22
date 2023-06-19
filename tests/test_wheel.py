import unittest
from product.Server import wheel


class TestWheel(unittest.TestCase):
    def test_spin(self):
        wheel_categories = ["Test1", "Test2", "Test3", "Test4", "Test5", "Test6"]

        my_wheel = wheel.Wheel(categories=wheel_categories)
        spin = my_wheel.spin()
        self.assertIn(spin, my_wheel.sectors)


if __name__ == '__main__':
    unittest.main()
