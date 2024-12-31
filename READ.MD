 
 sTART SERVER: 
npx eleventy --serve

 BUILD: 
eleventy

clear cache: 
rm -rf dist/ _site/


firebase deploy 

firebase deploy --only hosting


MINIFY:

html from root:
npx html-minifier --input-dir dist --output-dir dist --file-ext html --collapse-whitespace --remove-comments --minify-css true --minify-js true


git add .
git commit -m 'new'
git push



eleventy  firebase deploy --only hosting 