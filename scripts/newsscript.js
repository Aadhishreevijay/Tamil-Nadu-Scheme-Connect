const API_KEY = "9b3b73f6845c45a9bc9ca510ee45ea7f";
const url = "https://newsapi.org/v2/everything?q=";

// Listen for the page load event to fetch initial news
window.addEventListener("load", () => fetchNews("Government of India Tamil Nadu"));

// Reload function to refresh the page
function reload() {
    window.location.reload();
}

// Function to fetch news articles based on the query
async function fetchNews(query) {
    const res = await fetch(`${url}${query} Government of India&apiKey=${API_KEY}&language=en`);
    const data = await res.json();
    bindData(data.articles);
}

// Function to bind news data to the HTML
function bindData(articles) {
    const cardsContainer = document.getElementById("cards-container");
    const newsCardTemplate = document.getElementById("template-news-card");

    cardsContainer.innerHTML = "";

    articles.forEach((article) => {
        if (!article.urlToImage) return;
        const cardClone = newsCardTemplate.content.cloneNode(true);
        fillDataInCard(cardClone, article);
        cardsContainer.appendChild(cardClone);
    });
}

// Function to fill news data in the card template
function fillDataInCard(cardClone, article) {
    const newsImg = cardClone.querySelector("#news-img");
    const newsTitle = cardClone.querySelector("#news-title");
    const newsSource = cardClone.querySelector("#news-source");
    const newsDesc = cardClone.querySelector("#news-desc");

    newsImg.src = article.urlToImage;
    newsTitle.innerHTML = article.title;
    newsDesc.innerHTML = article.description;

    const date = new Date(article.publishedAt).toLocaleString("en-US", {
        timeZone: "Asia/Kolkata",
    });

    newsSource.innerHTML = `${article.source.name} · ${date}`;

    cardClone.firstElementChild.addEventListener("click", () => {
        window.open(article.url, "_blank");
    });
}

let curSelectedNav = null;

// Function to handle navigation item clicks
function onNavItemClick(id) {
    fetchNews(id + " Government of India Tamil Nadu");
    const navItem = document.getElementById(id);
    curSelectedNav?.classList.remove("active");
    curSelectedNav = navItem;
    curSelectedNav.classList.add("active");
}

// Handle search button click
const searchButton = document.getElementById("search-button");
const searchText = document.getElementById("search-text");

searchButton.addEventListener("click", () => {
    const query = searchText.value;
    if (!query) return;
    fetchNews(query + " Government of India Tamil Nadu");
    curSelectedNav?.classList.remove("active");
    curSelectedNav = null;
});
