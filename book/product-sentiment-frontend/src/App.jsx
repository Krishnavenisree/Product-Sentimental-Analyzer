import { useState } from "react";
import { scrapeBooks, getBooks } from "./api";
import {
  Chart as ChartJS,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";
import { Pie, Bar } from "react-chartjs-2";
import "./App.css";

ChartJS.register(
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
);

function App() {
  const [loading, setLoading] = useState(false);
  const [showDashboard, setShowDashboard] = useState(false);
  const [data, setData] = useState(null);
  const [books, setBooks] = useState([]);
  const [filterRating, setFilterRating] = useState(null);

  const handleScrape = async () => {
    setLoading(true);

    try {
      const result = await scrapeBooks();
      setData(result);

      // Fetch all books after scraping
      const allBooks = await getBooks();
      setBooks(allBooks);

      setShowDashboard(true);
    } catch (error) {
      alert("Backend error. Is Flask running?");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = async (rating) => {
    setFilterRating(rating);
    try {
      const filteredBooks = await getBooks(rating);
      setBooks(filteredBooks);
    } catch (error) {
      console.error(error);
    }
  };

  const ratingDist = data?.rating_distribution;

  const pieData =
    ratingDist && {
      labels: ["5 Stars", "4 Stars", "3 Stars", "2 Stars", "1 Star"],
      datasets: [
        {
          data: [
            ratingDist[5] || 0,
            ratingDist[4] || 0,
            ratingDist[3] || 0,
            ratingDist[2] || 0,
            ratingDist[1] || 0,
          ],
          backgroundColor: ["#4ade80", "#a3e635", "#fde047", "#fb923c", "#f87171"],
          borderWidth: 0,
        },
      ],
    };

  const barData =
    ratingDist && {
      labels: ["5 Stars", "4 Stars", "3 Stars", "2 Stars", "1 Star"],
      datasets: [
        {
          label: "Number of Books",
          data: [
            ratingDist[5] || 0,
            ratingDist[4] || 0,
            ratingDist[3] || 0,
            ratingDist[2] || 0,
            ratingDist[1] || 0,
          ],
          backgroundColor: "#7dd3fc",
          borderRadius: 6,
        },
      ],
    };

  return (
    <div className="app">
      {!showDashboard ? (
        <div className="input-box">
          <h1>📚 Book Scraper</h1>
          <p className="subtitle">Scrape books from books.toscrape.com</p>

          <button onClick={handleScrape}>
            {loading ? "Scraping..." : "Start Scraping"}
          </button>
        </div>
      ) : (
        <div className="dashboard">
          <h1 className="title">📚 Books Dashboard</h1>
          <p className="url">Data from books.toscrape.com</p>

          <div className="stats">
            <div className="stat-card">
              <h3>Total Books</h3>
              <p>{data.total_books}</p>
            </div>

            <div className="stat-card">
              <h3>Highest Rated</h3>
              <p>{ratingDist[5] || 0} books with 5⭐</p>
            </div>
          </div>

          <div className="charts">
            <div className="chart-card">
              <h3>Rating Distribution</h3>
              <div className="chart-wrapper">
                <Pie data={pieData} />
              </div>
            </div>

            <div className="chart-card">
              <h3>Rating Comparison</h3>
              <div className="chart-wrapper">
                <Bar data={barData} />
              </div>
            </div>
          </div>

          <div className="books-section">
            <h3>📖 Scraped Books</h3>

            <div className="filter-buttons">
              <button
                className={filterRating === null ? "active" : ""}
                onClick={() => handleFilterChange(null)}
              >
                All
              </button>
              {[5, 4, 3, 2, 1].map((r) => (
                <button
                  key={r}
                  className={filterRating === r ? "active" : ""}
                  onClick={() => handleFilterChange(r)}
                >
                  {r}⭐
                </button>
              ))}
            </div>

            <div className="books-grid">
              {books.slice(0, 20).map((book, index) => (
                <div key={index} className="book-card">
                  <h4>{book.title}</h4>
                  <p className="price">{book.price}</p>
                  <p className="rating">{"⭐".repeat(book.rating || 0)}</p>
                  <a href={book.url} target="_blank" rel="noreferrer">
                    View Book
                  </a>
                </div>
              ))}
            </div>

            {books.length > 20 && (
              <p className="more-info">Showing 20 of {books.length} books</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;