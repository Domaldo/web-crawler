# Import Web Crawling Dependencies
import requests
from bs4 import BeautifulSoup
# Import SQLite for storage of data as well as import Datetime for column
import sqlite3
from datetime import datetime
# Import regex for the proper filtering of words
import re

# Crawler Class
class HackerNewsCrawler:
    # Set up the URL for the crawler
    def __init__(self, url='https://news.ycombinator.com/'):
        self.url = url

    # Fetch the entries with the crawler and imported dependencies
    def fetch_entries(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        entries = []
        items = soup.find_all('tr', class_='athing')

        # Following Page Structure to fetch each item
        for item in items[:30]:  # Limiting to 30 entries
            entry = {}
            entry['rank'] = item.find('span', class_='rank').text.strip('.')
            title_tag = item.find('span', class_='titleline').find('a')
            entry['title'] = title_tag.text if title_tag else 'No title'

            subtext = item.find_next_sibling('tr').find('td', class_='subtext')
            points_tag = subtext.find('span', class_='score')
            entry['points'] = int(points_tag.text.split()[0]) if points_tag else 0

            comments_tag = subtext.find_all('a')[-1]
            comments_text = comments_tag.text.split()[0]
            entry['comments'] = int(comments_text) if comments_text.isdigit() else 0

            entries.append(entry)

        # Returning all values as a list
        return entries

# Database Class
class DatabaseManager:
    # Set database name, location in origin
    def __init__(self, db_name='hacker_news.db'):
        self.conn = sqlite3.connect(db_name)
        self.setup_database()

    # Table structure for database
    def setup_database(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hacker_news_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rank INTEGER,
                title TEXT,
                points INTEGER,
                comments INTEGER,
                timestamp TEXT
            )
        ''')
        self.conn.commit()

    # Function for saving data
    def save_entry(self, entry):
        cursor = self.conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO hacker_news_entries (rank, title, points, comments, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (entry['rank'], entry['title'], entry['points'], entry['comments'], timestamp))
        self.conn.commit()

    #Function for displaying data
    def get_all_entries(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM hacker_news_entries")
        return cursor.fetchall()

# Filter Class
class EntryFilter:
    @staticmethod
    def count_words(title):
        # Using regex to count words, ignoring symbols
        words = re.findall(r'\b\w[\w\'\-]*\w\b|\b\w\b', title)
        return len(words)

    def filter_by_word_count(self, entries, word_limit, filter_type):
        if filter_type == 'more_than':
            # Filter entries with more than "word_limit" words, in this case 5
            filtered_entries = [entry for entry in entries if self.count_words(entry['title']) > word_limit]
            # Sort filtered entries by number of comments in descending order
            return sorted(filtered_entries, key=lambda x: x['comments'], reverse=True)
        
        elif filter_type == 'less_than_equal':
            # Filter entries with "word_limit" or fewer words, in this case 5
            filtered_entries = [entry for entry in entries if self.count_words(entry['title']) <= word_limit]
            # Sort filtered entries by points in descending order
            return sorted(filtered_entries, key=lambda x: x['points'], reverse=True)

# Main Function
def main():
    # Initialize classes
    crawler = HackerNewsCrawler()
    db_manager = DatabaseManager()
    entry_filter = EntryFilter()

    # Fetch and save entries
    entries = crawler.fetch_entries()
    for entry in entries:
        db_manager.save_entry(entry)

    while True:  # Infinite loop to keep showing the menu
        # Options for the user
        print("\nChoose an option:")
        print("0 - Exit")
        print("1 - Show all entries")
        print("2 - Filter: More than 5 words, order by number of comments")
        print("3 - Filter: 5 or fewer words, order by points")
        
        choice = input("Enter your choice: ")

        if choice == '0':
            print("Exiting program.")
            break  # Exit the loop and end the program

        # Prints the entries from the database class functions
        elif choice == '1':
            all_entries = db_manager.get_all_entries()
            for entry in all_entries:
                print(entry)
        
        # Prints filtered entries from the database that have more than 5 words in their title, and orders them by the number of comments
        elif choice == '2':
            filtered = entry_filter.filter_by_word_count(entries, 5, 'more_than')
            for entry in filtered:
                print(entry)
        
        # Prints filtered entries from the database that have equal or less than 5 words in their title, and orders them by points
        elif choice == '3':
            filtered = entry_filter.filter_by_word_count(entries, 5, 'less_than_equal')
            for entry in filtered:
                print(entry)
        
        else:
            print("Invalid choice. Please enter 0, 1, 2, or 3.")

if __name__ == "__main__":
    main()