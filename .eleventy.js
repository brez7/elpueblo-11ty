module.exports = function (eleventyConfig) {
  // ✅ Copy everything from src/assets to dist/assets
  eleventyConfig.addPassthroughCopy("src/assets");

  // ✅ Blog post collection (optional)
  eleventyConfig.addCollection("posts", function (collectionApi) {
    return collectionApi.getFilteredByTag("posts").reverse();
  });

  return {
    dir: {
      input: "src", // Source folder
      output: "dist", // Output folder
      includes: "_includes", // Shortcodes, partials, etc.
      layouts: "_layouts", // Layout files
    },
    templateFormats: ["md", "njk", "html"], // File types to process
  };
};
