const functions = require("firebase-functions");
const {Client} = require("@googlemaps/google-maps-services-js");
const cors = require("cors")({origin: true}); // <- ✅ Add this line

const client = new Client({});
const apiKey = functions.config().google.key;

exports.getReviews = functions.https.onRequest((req, res) => {
  cors(req, res, async () => {
    const placeId = req.query.placeId;

    if (!placeId) {
      res.status(400).send("Missing placeId parameter");
      return;
    }

    if (!apiKey) {
      res
        .status(500)
        .send(
          'Missing Google API key. Use: firebase functions:config:set google.key="YOUR_API_KEY"'
        );
      return;
    }

    try {
      const response = await client.placeDetails({
        params: {
          place_id: placeId,
          fields: ["reviews"],
          key: apiKey,
        },
      });

      const reviews = response.data.result.reviews || [];
      res.status(200).json(reviews); // <- ✅ Make sure to use .json() here
    } catch (error) {
      console.error("Error fetching reviews:", error);
      res.status(500).send(`Error fetching reviews: ${error}`);
    }
  });
});
