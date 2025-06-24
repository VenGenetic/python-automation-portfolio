# Web Scraper for Books to Scrape

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python automation script that scrapes book data from [Books to Scrape](http://books.toscrape.com/) and exports it to an Excel file with statistical summary.

## Features

- Scrapes book titles, prices, ratings, and stock status
- Handles pagination automatically
- Robust error handling and retry mechanism
- Generates formatted Excel output with:
  - Raw data sheet
  - Statistical summary sheet
  - Auto-formatted headers
- Configurable delay between requests
- Comprehensive logging

## Installation

```bash
git clone https://github.com/yourusername/python-automation-portfolio.git
cd python-automation-portfolio/projects/web_scraper
pip install -r requirements.txt