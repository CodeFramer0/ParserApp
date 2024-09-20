import unittest

from utils import generate_combinations_of_replacements


class TestGenerateCombinationsOfReplacements(unittest.TestCase):
    def test_correct_replacements(self):
        s = "П-16054Б"
        expected = "П-160646"
        result = generate_combinations_of_replacements(s)
        self.assertIn(expected, result, f"Expected '{expected}' to be in {result}")

    def test_string_starting_with_I(self):
        s = "И-01554Б"
        expected = "И-016646"
        result = generate_combinations_of_replacements(s)
        self.assertIn(expected, result, f"Expected '{expected}' to be in {result}")

    def test_string_with_no_target_chars(self):
        s = "И-123456"
        expected_results = ["И-123456"]
        result = generate_combinations_of_replacements(s)
        self.assertTrue(
            set(expected_results).issubset(result),
            f"Expected results {expected_results} to be a subset of {result}",
        )

    def test_string_without_replacements(self):
        s = "П-123456"
        expected_results = ["П-123456"]
        result = generate_combinations_of_replacements(s)
        self.assertTrue(
            set(expected_results).issubset(result),
            f"Expected results {expected_results} to be a subset of {result}",
        )


if __name__ == "__main__":
    unittest.main()
