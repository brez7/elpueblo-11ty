module.exports = function (eleventyConfig) {
  // Copy assets (CSS, JS, images) to the output folder
  eleventyConfig.addPassthroughCopy("src/assets");

  // Create a collection for blog posts
  eleventyConfig.addCollection("blog", function (collectionApi) {
    return collectionApi.getFilteredByGlob("src/posts/*.md").reverse();
  });

  return {
    dir: {
      input: "src", // The main input directory
      output: "dist", // Where the final site is built
      includes: "_includes", // Where components are stored
      layouts: "_layouts", // Where layouts (base.njk) are stored
    },
    templateFormats: ["md", "njk", "html"], // Ensure Markdown is processed
  };
};
