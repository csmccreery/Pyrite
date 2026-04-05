import unittest
from src.literal_token import LiteralToken

class TestLiteralToken(unittest.TestCase):
    def test_create_token(self):
        literal_token = LiteralToken()
        self.assertTrue(literal_token is not None)
