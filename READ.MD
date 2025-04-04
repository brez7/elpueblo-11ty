 

guide me through step by step, waiting for me to type next to continue

contact-form-api

 sTART SERVER: 
npx eleventy --serve
npm run run

 BUILD: 
eleventy

clear cache: 
rm -rf dist/ _site/


firebase deploy 

firebase deploy --only hosting


MINIFY:

html from root:
npx html-minifier --input-dir dist --output-dircd  dist --file-ext html --collapse-whitespace --remove-comments --minify-css true --minify-js true


git add .
git commit -m 'new'
git push

FORM:
cd .\contact-form-api 

docker build -t contact-form-api .; docker tag contact-form-api us-central1-docker.pkg.dev/upbeat-button-265722/elpueblo-docker-repo/contact-form-api; docker push us-central1-docker.pkg.dev/upbeat-button-265722/elpueblo-docker-repo/contact-form-api; gcloud run deploy contact-form-api --image=us-central1-docker.pkg.dev/upbeat-button-265722/elpueblo-docker-repo/contact-form-api --platform=managed --region=us-central1 --allow-unauthenticated





eleventy  firebase deploy --only hosting 
npm run go

 

Chat GPT Prompts: 


Set Context

**Project Understanding**  
Read the README.md and summarize what this project does  
Scan the file structure and tell me what kind of app this is  
Based on the folder structure, what are the major parts of the project  
Are there any API endpoints defined in this codebase  
What does the main entry file do  

**Code Insight**  
Read index.js and explain its function  
Look at all files in the routes/ folder and list the endpoints  
Summarize what config.js is setting up  
Which files handle database operations  

**Project Status Awareness**  
What are the last 5 files that were changed  
What has been worked on in the last 3 days  
Which files have been edited most recently  

**Smart Workflow Prompts**  
Review my latest commit and suggest improvements  
Suggest next steps based on the project structure  
Where would I add a new route  
Where is the best place to configure middleware or environment variables  

**Advanced (when more features are added)**  
Summarize the difference between the last two commits  
Is there any unused code in this repo  
Generate docstrings for every exported function in this file


> “Here’s the context of my Eleventy project. Please load this.”  
> *(Then paste contents of this file.)*
