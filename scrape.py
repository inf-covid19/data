import time
import traceback

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


if __name__ == "__main__":
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
    ]

    for fn in scraper:
        executor(fn)
