import unittest
from main.web_crawler import HackerNewsCrawler, DatabaseManager, EntryFilter

class TestCrawler(unittest.TestCase):
    def setUp(self):
        print("\nRunning TestCrawler...")

    def test_fetch_entries(self):
        # Test if exactly 30 entries are fetched from Hacker News
        crawler = HackerNewsCrawler()
        entries = crawler.fetch_entries()
        self.assertEqual(len(entries), 30)
        print("TestCrawler: test_fetch_entries passed")

class TestFilter(unittest.TestCase):
    def setUp(self):
        print("\nRunning TestFilter...")

    def test_word_count(self):
        # Test if word counting works as expected, including symbols and hyphenation
        entry_filter = EntryFilter()
        self.assertEqual(entry_filter.count_words("ChatGPT? is cool"), 3)
        self.assertEqual(entry_filter.count_words("this-word"), 1)
        print("TestFilter: test_word_count passed")

class TestDatabase(unittest.TestCase):
    def setUp(self):
        print("\nRunning TestDatabase...")

    def test_database_operations(self):
        # Use in-memory SQLite database for testing
        db_manager = DatabaseManager(':memory:')  # ':memory:' creates a temp DB for testing
        entry = {'rank': 1, 'title': 'Test Entry', 'points': 100, 'comments': 50}
        
        # Save and retrieve entry from the database
        db_manager.save_entry(entry)
        results = db_manager.get_all_entries()
        
        # Check that the entry was saved and retrieved correctly
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][2], 'Test Entry')  # Check that title matches
        print("TestDatabase: test_database_operations passed")

if __name__ == "__main__":
    unittest.main()
