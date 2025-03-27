document.addEventListener("DOMContentLoaded", async () => {
  const reviewsContainer = document.getElementById("reviews");

  const placeId = "ChIJp_33wbgJ3IARqR-3nQO0Jng";
  const endpoint = `https://us-central1-restart-elpueblo.cloudfunctions.net/getReviews?placeId=${placeId}`;

  try {
    const res = await fetch(endpoint);
    const reviews = await res.json();

    if (!Array.isArray(reviews)) throw new Error("Invalid review format");

    // Create a grid container for all review cards
    const grid = document.createElement("div");
    grid.className = "review-grid";

    reviews.forEach(review => {
      const card = document.createElement("div");
      card.className = "review-card";

      const stars = "⭐️".repeat(Math.round(review.rating));

      card.innerHTML = `
        <div class="review-header">
          <img src="${review.profile_photo_url}" alt="${review.author_name}" class="review-photo" />
          <div>
            <h4>${review.author_name}</h4>
            <p class="review-stars">${stars}</p>
          </div>
        </div>
        <p class="review-text">"${review.text}"</p>
      `;

      grid.appendChild(card);
    });

    reviewsContainer.innerHTML = ""; // Clear any loading text
    reviewsContainer.appendChild(grid); // Add all reviews to the container
  } catch (err) {
    console.error("Error fetching reviews:", err);
    reviewsContainer.innerHTML = "<p>Could not load reviews right now.</p>";
  }
});
