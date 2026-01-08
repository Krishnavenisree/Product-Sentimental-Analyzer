import time
import csv
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# ================== DRIVER SETUP ==================
def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


# ================== RATING EXTRACTION (books.toscrape specific) ==================
def extract_rating_from_class(block):
    # books.toscrape uses classes like "star-rating Three"
    star_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    p = block.select_one("p.star-rating")
    if not p:
        return None
    for cls in p.get("class", []):
        if cls in star_map:
            return star_map[cls]
    return None


# ================== SCRAPE ONE PAGE ==================
def scrape_books_from_page(driver, page_url):
    driver.get(page_url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    book_blocks = soup.select("article.product_pod")
    page_books = []

    for b in book_blocks:
        # Title and relative link
        a = b.select_one("h3 > a")
        title = a.get("title") or a.text.strip()
        href = a.get("href")
        product_url = urljoin(page_url, href)

        # Price
        price_tag = b.select_one("p.price_color")
        price = price_tag.text.strip() if price_tag else None

        # Rating
        rating = extract_rating_from_class(b)

        page_books.append({
            "title": title,
            "price": price,
            "rating": rating,
            "url": product_url
        })

    # detect next page link (relative)
    next_link = None
    next_tag = soup.select_one("li.next > a")
    if next_tag:
        next_link = urljoin(page_url, next_tag.get("href"))

    return page_books, next_link


# ================== HELPERS FOR RANDOM PAGES ==================
def get_total_pages(driver, start_url):
    """Return total number of pages reported by the site's pagination.

    Looks for a `li.current` element that usually contains text like
    'Page 1 of 50' and extracts the last integer. Falls back to 1.
    """
    driver.get(start_url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    current = soup.select_one("li.current")
    if current and current.text:
        text = current.text.strip()
        parts = text.split()
        try:
            total = int(parts[-1])
        except Exception:
            total = 1
    else:
        total = 1
    return total


def build_page_url(start_url, page_number):
    """Construct a page URL for the given page number.

    - page 1 returns start_url
    - page >1 uses the common books.toscrape pattern: catalogue/page-<n>.html
    """
    if page_number == 1:
        return start_url
    return urljoin(start_url, f"catalogue/page-{page_number}.html")


def scrape_random_pages(start_url, max_pages=10):
    """Scrape up to `max_pages` random, non-repeating pages from the site.

    This samples page numbers without replacement based on the total
    pages discovered from the site's pagination. Returns the collected
    book items.
    """
    driver = setup_driver()
    all_books = []

    try:
        total_pages = get_total_pages(driver, start_url)
        pages_to_fetch = min(max_pages, total_pages)

        # sample unique page numbers
        page_numbers = random.sample(range(1, total_pages + 1), k=pages_to_fetch)

        print(f"🔀 Selected random pages: {page_numbers}")

        for idx, pn in enumerate(page_numbers, start=1):
            page_url = build_page_url(start_url, pn)
            print(f"➡️  Fetching random page {idx} (page {pn}): {page_url}")
            books, _ = scrape_books_from_page(driver, page_url)
            if not books:
                # skip empty pages but continue
                continue
            all_books.extend(books)
            time.sleep(1)
    finally:
        driver.quit()

    print(f"✅ Total Books Scraped (random): {len(all_books)}")
    return all_books


# ================== SCRAPE ALL PAGES ==================
def scrape_all_books(start_url, max_pages=10):
    driver = setup_driver()
    all_books = []
    url = start_url
    page_count = 0

    print("🔎 Scraping books.toscrape.com...")

    try:
        while url and page_count < max_pages:
            page_count += 1
            print(f"➡️  Fetching page {page_count}: {url}")
            books, next_url = scrape_books_from_page(driver, url)
            if not books:
                break
            all_books.extend(books)
            url = next_url
            # small delay between pages
            time.sleep(1)
    finally:
        driver.quit()

    print(f"✅ Total Books Scraped: {len(all_books)}")
    return all_books


# ================== SAVE TO CSV ==================
def save_to_csv(items, filename="books.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["S.No", "Title", "Price", "Rating", "Product URL"])
        for i, it in enumerate(items, start=1):
            writer.writerow([
                i,
                it.get("title"),
                it.get("price"),
                it.get("rating"),
                it.get("url")
            ])


# ================== MAIN ==================
if __name__ == "__main__":
    START_URL = "http://books.toscrape.com/"

    # By default, scrape random non-repeating pages instead of sequential pages.
    # Adjust `max_pages` if you want more or fewer sampled pages.
    books = scrape_random_pages(START_URL, max_pages=10)

    save_to_csv(books, "books_toscrape.csv")

    df = pd.DataFrame(books)
    print(df.head())

    print(f"\n� Total books: {len(books)}")