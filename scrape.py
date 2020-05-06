import time
import traceback
import argparse


from helpers import executor

from countries import scrape_countries
from brazil import scrape_brazil
from sweden import scrape_sweden
from united_states_of_america import scrape_united_states_of_america
from spain import scrape_spain
from united_kingdom import scrape_united_kingdom
from chile import scrape_chile
from bolivia import scrape_bolivia
from argentina import scrape_argentina
from ecuador import scrape_ecuador
from colombia import scrape_colombia
from peru import scrape_peru
from uruguay import scrape_uruguay


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape COVID-19 cases and deaths.')
    parser.add_argument('-r', '--region', nargs="+", help="regions to scrape")

    args = parser.parse_args()

    scraper = [
        scrape_countries,
        scrape_brazil,
        scrape_sweden,
        scrape_united_states_of_america,
        scrape_spain,
        scrape_united_kingdom,
        scrape_chile,
        scrape_bolivia,
        scrape_argentina,
        scrape_ecuador,
        scrape_colombia,
        scrape_peru,
        scrape_uruguay,
    ]

    if args.region is not None:
        scraper = [fn for fn in scraper if len(
            [r for r in args.region if r in fn.__name__]) > 0]

    for fn in scraper:
        executor(fn)
