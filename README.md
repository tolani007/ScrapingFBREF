Premier League Match Data Scraper (SUPERFBREFSCRAPER)

Overview

This Python script automates the scraping of Premier League match data from FBref, collecting team statistics such as shooting, passing, defense, and possession over multiple seasons. It includes checkpointing, user-agent rotation, and backoff delays to ensure efficiency and avoid anti-scraping measures.

Key Features

✅ Scrapes match stats across multiple seasons and teams.✅ Handles rate limits with smart retries and exponential backoff.✅ Uses rotating User-Agent headers for stealthy requests.✅ Stores data in CSV format for easy analysis.✅ Implements a checkpoint system to resume failed scrapes.

Installation & Setup

1. Install Dependencies

Ensure you have Python installed, then run:

pip install -r requirements.txt

Or manually install:

pip install requests pandas beautifulsoup4 fake-useragent

2. Run the Script

python scraper.py

Interactive Web UI

Want to trigger scrapes from the browser? An interactive front end powered by Flask is included:

1) Install the requirements (see above).
2) Start the server:

python app.py

3) Open http://localhost:8000 to enter a season (e.g., 2023-2024) and scrape fixtures directly from FBref.

How It Works

1. Checkpoint System

Saves progress in scraper_checkpoint.json to resume failed runs.

Skips already scraped teams and seasons.

2. Smart Request Handling

Uses fake-useragent to randomize User-Agent headers.

Adds random delays (20-40s) between requests to reduce detection.

Uses backoff delays (300-720s) for handling rate-limiting.

3. Data Collection Process

Retrieves season standings and extracts team URLs.

Scrapes match results, shooting, passing, defensive, and possession data.

Merges all statistics and appends to matches.csv.

4. Error Handling & Retry Logic

Retries failed requests up to 5 times with increasing wait times.

If still unsuccessful, waits 1 hour and retries once more.

If final attempt fails, logs the issue and moves to the next team.

File Structure

📂 project_root
├── scraper.py            # Main script
├── requirements.txt      # Python dependencies
├── scraper_checkpoint.json # Stores last successful scrape (auto-generated)
└── matches.csv           # Scraped data output (auto-generated)

Customization

Modify Seasons to Scrape

Edit seasons_to_scrape in scraper.py:

seasons_to_scrape = [
    "2017-2018", "2018-2019", "2019-2020",
    "2020-2021", "2021-2022", "2022-2023", "2023-2024"
]

Enable Proxy Support

To use a proxy, modify this line in fetch_with_backoff():

use_proxy = True

Replace "http://your_proxy:port" with your actual proxy settings.

Troubleshooting

1. Script Stops Midway

Restarting the script will resume from the last checkpoint.

2. Blocked by FBref?

Try changing your User-Agent or using a VPN/proxy.

Reduce request frequency by increasing delay time:

randomized_delay(min_delay=30, max_delay=60)

Future Improvements

🔹 Enhance analytics with expected goals (xG), expected assists (xA), and pressing stats.🔹 Implement multi-threading for faster scraping.🔹 Store data in a database instead of CSV.

Contributing

Fork, modify, and improve this project. Found a bug or want a new feature? Submit a pull request!

License

This project is open-source under the MIT License.

🚀 Happy scraping!

