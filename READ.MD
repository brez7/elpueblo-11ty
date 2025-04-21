guide me through step by step, waiting for me to type go to continue

test

# start remote vsc xx
Remote-SSH: Connect to Host...
select: remote-dev

# Manual pull from remote
SFTP: Download Project

https://vscode.dev/tunnel/remote-dev-vm/home/mexicanfoodelpueblo/yummy-elpueblo-11ty

cd contact-form-api

START SERVER:
npx eleventy --serve
npm run run

BUILD:
eleventy
 
clear cache:
rm -rf dist/ \_site/

firebase deploy

firebase deploy --only hosting

MINIFY:

html from root:
npx html-minifier --input-dir dist --output-dircd dist --file-ext html --collapse-whitespace --remove-comments --minify-css true --minify-js true

git add .
git commit -m 'new'
git push

FORM:
cd .\contact-form-api

docker build -t contact-form-api .; docker tag contact-form-api us-central1-docker.pkg.dev/upbeat-button-265722/elpueblo-docker-repo/contact-form-api; docker push us-central1-docker.pkg.dev/upbeat-button-265722/elpueblo-docker-repo/contact-form-api; image=us-central1-docker.pkg.dev/upbeat-button-265722/elpueblo-docker-repo/contact-form-api:v2 --platform=managed --region=us-central1 --allow-unauthenticated

eleventy firebase deploy --only hosting
npm run go

pro url:
fetch("https://contact-form-api-fvmy7faymq-uc.a.run.app/reviews")
