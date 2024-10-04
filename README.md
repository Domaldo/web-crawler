# web-crawler

This web crawler fetches submissions from [Hacker News](https://news.ycombinator.com/), saves the entries into an SQLite database, and allows filtering of entries based on the length in words of the title, while ordering them by either number of comments or points of each entry.

## Installation

### Requirements
- Python 3.x
- Pip (Python package installer)

### Setup

1. **Clone the repository:**  
   Download or clone this repository to your local machine.

2. **Navigate to the project directory:**  
   Open a terminal or PowerShell window and navigate to the project folder:
   ```bash
   cd .../web-crawler-main

3. **Install dependencies:**  
   To install the required Python packages (`requests`, `bs4`, etc.), run the following command:
   ```bash
   pip install -r requirements.txt
   ```
   This command ensures all necessary third-party libraries are installed.

4. **Run the Web-Crawler:**  
   To execute the web crawler and interact with the program, run::
   ```bash
   python main\web_crawler.py
   ```
   This command starts the program and will prompt you to select options to fetch, view, or filter the Hacker News data.
   
5. **Run automated tests:**  
   To execute the project's unit tests, run:
   ```bash
   python -m unittest discover tests
   ```
   This command discovers and runs all tests in the `tests` folder. Unit tests are designed to verify that the core functionalities of the program (such as fetching entries, filtering, and database operations) are working correctly.

## Features

- Fetches up to 30 entries from the Hacker News main page.
- Saves entries (rank, title, points, comments & timestamp) into an SQLite database.
- Filters entries in two ways:
    - Filters entries with more than five words in the title, ordered by the number of comments.
    - Filters entries with five or fewer words in the title, ordered by points.

## Project Structure

```bash
web-crawler-main/
│
├── main/
│   ├── __init__.py
│   └── web_crawler.py          # Main program logic
│
├── tests/
│   ├── __init__.py
│   └── test_hackernews.py       # Unit tests for the project
├── .gitignore
├── README.md                    # Project documentation
└── requirements.txt             # List of project dependencies
```

## Notes
- **Python modules:** Some standard modules like `re` and `sqlite3` should come pre-installed with Python. However, `requests` and `bs4` must be installed using pip. To ensure nothing is missing, all of these are listed in the `requirements.txt` file.

- **.gitignore:** This project includes a `.gitignore` file to prevent certain files (such as the SQLite database and Python cache files) from being tracked in version control.

## License
This project is open-source and free to use under the MIT license.