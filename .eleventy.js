const {DateTime} = require("luxon");

module.exports = function (eleventyConfig) {
  // ✅ Passthrough for static assets (images, CSS, etc.)
  eleventyConfig.addPassthroughCopy("src/assets");

  // ✅ Full blog collection (all posts tagged "blog", newest first)
  eleventyConfig.addCollection("blog", function (collectionApi) {
    return collectionApi.getFilteredByTag("blog").reverse();
  });

  // ✅ Date formatting filter using Luxon
  eleventyConfig.addFilter("date", (value, format = "MMMM d, yyyy") => {
    return DateTime.fromJSDate(value, {zone: "utc"}).toFormat(format);
  });

  // ✅ Eleventy directory structure and file format setup
  return {
    dir: {
      input: "src",
      output: "dist",
      includes: "_includes",
      layouts: "_layouts",
    },
    templateFormats: ["md", "njk", "html"],
  };
};
