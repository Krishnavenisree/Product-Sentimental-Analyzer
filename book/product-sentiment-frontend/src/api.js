const API_BASE_URL = "https://book-l8eb.onrender.com";

export async function scrapeBooks(startUrl = "http://books.toscrape.com/") {
  const response = await fetch(`${API_BASE_URL}/scrape`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      start_url: startUrl,
    }),
  });

  if (!response.ok) {
    throw new Error("Backend error");
  }

  return await response.json();
}

export async function getBooks(rating = null) {
  const url = rating
    ? `${API_BASE_URL}/books?rating=${rating}`
    : `${API_BASE_URL}/books`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Backend error");
  }

  return await response.json();
}