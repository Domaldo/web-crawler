# Import Web Crawling Dependencies
import requests
from bs4 import BeautifulSoup

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

# Main Function
def main():
    # Initialize classes
    crawler = HackerNewsCrawler()

    # Fetch entries
    entries = crawler.fetch_entries()

    while True:  # Infinite loop to keep showing the menu
        # Options for the user
        print("\nChoose an option:")
        print("0 - Exit")
        print("1 - Show all entries")
        
        choice = input("Enter your choice: ")

        if choice == '0':
            print("Exiting program.")
            break  # Exit the loop and end the program

        # Fetches and prints all entries one by one
        elif choice == '1':
            for entry in entries:
                print(entry)
        
        else:
            print("Invalid choice. Please enter 0 or 1.")

if __name__ == "__main__":
    main()