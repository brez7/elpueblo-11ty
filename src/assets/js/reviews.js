document.addEventListener("DOMContentLoaded", async () => {
  const reviewsContainer = document.getElementById("reviews");
  if (!reviewsContainer) {
    console.error("❌ #reviews container is missing from the DOM.");
    return;
  }

  const endpoint =
    "https://contact-form-api-fvmy7faymq-uc.a.run.app/reviews?refresh=true";

  try {
    const res = await fetch(endpoint);
    const data = await res.json();

    console.log("✅ Fetched review data:", data);

    const reviews = data.reviews || [];

    if (!Array.isArray(reviews)) throw new Error("Invalid review format");

    const grid = document.createElement("div");
    grid.className = "review-grid";

    reviews.forEach(review => {
      const stars = "⭐️".repeat(
        review.starRating === "FIVE"
          ? 5
          : review.starRating === "FOUR"
          ? 4
          : review.starRating === "THREE"
          ? 3
          : review.starRating === "TWO"
          ? 2
          : 1
      );

      const card = document.createElement("div");
      card.className = "review-card";

      card.innerHTML = `
        <div class="review-header">
          <img src="${
            review.reviewer?.profilePhotoUrl || "/assets/img/google.svg"
          }"
               alt="${review.reviewer?.displayName || "Anonymous"}" 
               class="review-photo" 
               onerror="this.src='/assets/img/google.svg';" />
          <div>
            <h4>${review.reviewer?.displayName || "Anonymous"}</h4>
            <p class="review-stars">${stars}</p>
          </div>
        </div>
        <p class="review-text">"${review.comment || ""}"</p>
      `;

      grid.appendChild(card);
    });

    reviewsContainer.innerHTML = "";
    reviewsContainer.appendChild(grid);
  } catch (err) {
    console.error("❌ Error fetching reviews:", err);
    reviewsContainer.innerHTML = "<p>Could not load reviews right now.</p>";
  }
});
