from countries import scrape_countries
from brazil import scrape_brazil
import time

def scrape(fn):
    print(f'[{fn.__name__}] Starting...')
    start_time = time.time()
    fn()
    elapsed_time = time.time() - start_time
    print(f'[{fn.__name__}] Done in {elapsed_time:.3f}s!')


if __name__ == "__main__":
    scrape(scrape_countries)
    scrape(scrape_brazil)
