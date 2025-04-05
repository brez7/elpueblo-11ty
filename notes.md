Here’s the context of my Eleventy project. Please load this. 

# 📘 Eleventeenth Project Context — `elpueblo-11ty`

You began by building two form endpoints—/submit for contact messages and /reserve for party reservations—using Flask, hosted on Google Cloud Run, and integrated with Google Sheets and Gmail. The backend was Dockerized, and deployment was managed via gcloud run deploy.

Initially, the reservation form was returning CORS and 404 errors, even though the route was correctly defined in app.py. You verified the route with @app.route("/reserve", methods=["POST", "OPTIONS"]) and ensured CORS headers were set. The real issue turned out to be Cloud Run not serving the most recent image despite rebuilding with docker build. This was fixed by using versioned tags like v10, v200, and deploying them cleanly, avoiding image cache issues with --no-cache.

Another problem was with how you tested the routes using curl in PowerShell. Many errors stemmed from PowerShell syntax differences (like backticks and escaping quotes), which led to confusing 400 and 404 errors. Eventually, you tested the endpoints successfully using both curl and Invoke-RestMethod.

You also ran into a confusing situation where the contact form stopped working, while the reservation form worked fine. After investigating, you discovered the contact form was still pointing to the old Cloud Run URL (abc123), while the reservation form had the updated one (v200). Once you corrected the endpoint in contact.njk, both forms worked properly.

Ultimately, the main problems were outdated frontend URLs, Docker image caching, and inconsistent deployment. These were resolved by confirming route definitions, verifying deployed versions, and syncing frontend service URLs.

Now both forms are working, and the stack is running smoothly on Cloud Run with email notifications and Google Sheets logging fully functional.

You’re working on an Eleventy-based static site with a Flask API deployed to Google Cloud Run. After successfully deploying a working /submit contact form endpoint, you built a new /reserve endpoint to handle party reservation form data. Despite validating the route existed in your Docker build, hitting /reserve on Cloud Run consistently returned a 404 error, which initially appeared to be a CORS issue.

After investigation, it became clear that the actual problem was that Cloud Run was serving an older version of your container — one that didn’t include /reserve. Even though you rebuilt the Docker image and tagged it :v2, Cloud Run kept deploying the same image digest (sha256:3cf3...). This meant your changes weren’t reaching production.

We confirmed that the issue stemmed from gcloud crashing during deploy due to a Windows-specific OSError: [Errno 22] Invalid argument, related to terminal encoding. This crash silently prevented your gcloud run deploy command from finishing successfully.

To resolve this:

You set PowerShell’s output encoding using $OutputEncoding = [System.Text.Encoding]::UTF8

Then rebuilt the Docker image using a fresh tag like :v3

Pushed it to Artifact Registry

Explicitly deployed the new image using the full tag with gcloud run deploy

You were instructed to verify the new revision in the Cloud Run console and test the route using PowerShell curl. This cleaned up any image caching issues and ensured /reserve is now correctly deployed and live.
You began by setting up an Eleventy (11ty) static site and integrating a contact form backend using Python Flask, deployed via Google Cloud Run. You created a contact-form-api with Flask, using Gmail SMTP for email delivery, and later added Google Sheets logging to track submissions. The backend correctly handled POST requests at /submit, verified using curl in both WSL and PowerShell environments.

We debugged several deployment and runtime issues. Early errors involved Cloud Run deployment failures due to image access from Google Container Registry (GCR), which is deprecated. We resolved this by pushing the Docker image to Artifact Registry instead. You also encountered an issue with secret scanning when trying to push the sheets-creds.json file to GitHub — GitHub's push protection blocked it due to it containing Google service credentials. We handled this by using .gitignore, removing the file from Git's index, and cleaning up commit history.

You successfully installed and ran Gunicorn within WSL to serve your Flask app. When transitioning to include Google Sheets, we configured OAuth scopes and used gspread and google-auth for appending form data to your spreadsheet. We overcame a submit() route duplication bug and installation errors related to distutils packages like blinker.

We updated the contact form logic so emails are sent to both rob@elpueblomex.com and rob@barbank.com, and added a confirmation email to be sent back to the person who filled out the form. Docker deployment scripts were tested and iterated on, with emphasis on inline PowerShell-compatible commands for tagging, pushing, and deploying.

Throughout the session, we reinforced using best practices for secrets management, deployment hygiene, and debugging Flask + Gunicorn issues on WSL.

You now have a fully functional contact form API that logs to Google Sheets, sends email notifications to admins, and sends confirmations to users.

In this session, we set up a fully customizable contact form for an Eleventy static site using a Flask API deployed on Google Cloud Run. After evaluating options, we chose Flask over Firebase Functions for greater flexibility and control. We built the Flask app with a /submit endpoint to handle POST requests, containerized it with Docker, and deployed it to Cloud Run using the Google Cloud CLI.

To handle browser security restrictions, we addressed a CORS error by integrating flask-cors and explicitly allowing cross-origin requests. Once the API was live, we wired up a frontend form in the Eleventy site to send submissions via fetch.

Next, we enabled Gmail integration by generating a secure App Password for it@elpueblomex.com and configured Flask to send emails via SMTP. After successful deployment and testing, we verified that the contact form was sending emails properly.

We also began integrating Google Sheets as a backend log for form submissions. This involved creating a new Google Sheet, setting up a service account, enabling the Google Sheets API, and preparing secure authentication credentials to allow Flask to write data to the sheet.

The session was highly productive, ending with a live contact form that sends real emails and is nearly ready for full data logging.

Always use thsi styling for buttons: 

.btn-read-more {
  background: #7f120b;
  color: white;
  border: 1px solid black;
  padding: 10px 28px 12px 28px;
  border-radius: 50px;
  font-weight: 400;
  font-size: 15px;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.1);
  transition: 0.5s;
  letter-spacing: 1px;
}

## 🧠 Project Purpose

This is a content-rich static site built with [11ty (Eleventy)](https://11ty.dev). It integrates:
- Custom GitHub polling logic via Python
- Firebase Hosting + optional Cloud Functions
- Custom templates and layouts for content like locations, menus, and blog-style posts

The project uses a structured source folder and a Python-based data fetcher to pull GitHub info into Eleventy templates dynamically.

---

## 📁 Directory Structure Overview

```
Project Structure:

├── READ.MD
├── code-pull-index.html
├── design-source
│   └── image-template.psd
├── dist
│   ├── assets
│   │   ├── css
│   │   │   ├── custom.css
│   │   │   ├── main.css
│   │   │   └── vendor.min.css
│   │   ├── img
│   │   │   ├── about-2.jpg
│   │   │   ├── about.jpg
│   │   │   ├── apple-touch-icon.png
│   │   │   ├── blog
│   │   │   │   ├── bunuelos.jpg
│   │   │   │   ├── dinner-plate.jpg
│   │   │   │   └── dinner.jpg
│   │   │   ├── carne-asada.png
│   │   │   ├── carneasada plate.png
│   │   │   ├── chefs
│   │   │   │   ├── chefs-1.jpg
│   │   │   │   ├── chefs-2.jpg
│   │   │   │   └── chefs-3.jpg
│   │   │   ├── el-pueblo-logo.png
│   │   │   ├── el_pueblo_mex_logo-01.png
│   │   │   ├── events-1.jpg
│   │   │   ├── events-2.jpg
│   │   │   ├── events-3.jpg
│   │   │   ├── events-4.jpg
│   │   │   ├── favicon.png
│   │   │   ├── gallery
│   │   │   │   ├── gallery-1.jpg
│   │   │   │   ├── gallery-2.jpg
│   │   │   │   ├── gallery-3.jpg
│   │   │   │   ├── gallery-4.jpg
│   │   │   │   ├── gallery-5.jpg
│   │   │   │   ├── gallery-6.jpg
│   │   │   │   ├── gallery-7.jpg
│   │   │   │   └── gallery-8.jpg
│   │   │   ├── hero-img.png
│   │   │   ├── logo.png
│   │   │   ├── menu
│   │   │   │   ├── menu-item-1.png
│   │   │   │   ├── menu-item-2.png
│   │   │   │   ├── menu-item-3.png
│   │   │   │   ├── menu-item-4.png
│   │   │   │   ├── menu-item-5.png
│   │   │   │   └── menu-item-6.png
│   │   │   ├── menu-items
│   │   │   │   ├── 2-for-10-taco-combo.jpg
│   │   │   │   ├── adobada-burrito.jpg
│   │   │   │   ├── adobada-quesadilla.jpg
│   │   │   │   ├── adobada-taco.jpg
│   │   │   │   ├── adobada-torta.jpg
│   │   │   │   ├── bean-and-cheese-burrito.jpg
│   │   │   │   ├── breakfast-bowl.jpg
│   │   │   │   ├── breakfast-burrito.jpg
│   │   │   │   ├── breakfast.jpg
│   │   │   │   ├── cali-burrito.jpg
│   │   │   │   ├── carne-asada-burrito.jpg
│   │   │   │   ├── carne-asada-plate.jpg
│   │   │   │   ├── carne-asada-quesadilla.jpg
│   │   │   │   ├── carne-asada-taco.jpg
│   │   │   │   ├── carne-asada-torta.jpg
│   │   │   │   ├── carnitas-burrito.jpg
│   │   │   │   ├── carnitas-burrito2.jpg
│   │   │   │   ├── carnitas-plate.jpg
│   │   │   │   ├── carnitas-quesadilla.jpg
│   │   │   │   ├── carnitas-taco.jpg
│   │   │   │   ├── carnitas-torta.jpg
│   │   │   │   ├── cheese-quesadilla.jpg
│   │   │   │   ├── chickentortsoup.jpg
│   │   │   │   ├── chilaquiles-rojos.jpg
│   │   │   │   ├── chilaquiles-verdes.jpg
│   │   │   │   ├── chile-relleno-burrito.jpg
│   │   │   │   ├── chile-relleno-plate.jpg
│   │   │   │   ├── chile-relleno.jpg
│   │   │   │   ├── chimichanga.jpg
│   │   │   │   ├── chips-and-salsa.jpg
│   │   │   │   ├── chorizo-burrito.jpg
│   │   │   │   ├── chorizo-plate.jpg
│   │   │   │   ├── chorizo-torta.jpg
│   │   │   │   ├── conga-burrito.jpg
│   │   │   │   ├── dinners.jpg
│   │   │   │   ├── el-pueblo-mexican-food.jpg
│   │   │   │   ├── el-pueblo-torta-with-fries.jpg
│   │   │   │   ├── enchiladas.jpg
│   │   │   │   ├── fajitas-burrito.jpg
│   │   │   │   ├── fajitas-plate.jpg
│   │   │   │   ├── fish-taco.jpg
│   │   │   │   ├── fish_tacos.jpg
│   │   │   │   ├── flautas-(3).jpg
│   │   │   │   ├── fries-and-chips.jpg
│   │   │   │   ├── full-menu.jpg
│   │   │   │   ├── guacamole-(1-2-tray).jpg
│   │   │   │   ├── ham-and-cheese.jpg
│   │   │   │   ├── huevos-a-la-mexicana.jpg
│   │   │   │   ├── huevos-con-jamon.jpg
│   │   │   │   ├── huevos-rancheros.jpg
│   │   │   │   ├── josh-cellars-vintage-pinot-noir-bottle-central-coast-(750-ml).jpg
│   │   │   │   ├── kids-quesadilla.jpg
│   │   │   │   ├── la-marca-prosecco-bottle-doc-italy-(375-ml).jpg
│   │   │   │   ├── lengua-taco.jpg
│   │   │   │   ├── machaca-burrito.jpg
│   │   │   │   ├── machaca-plate.jpg
│   │   │   │   ├── machaca-torta.jpg
│   │   │   │   ├── make-your-own-tacos.jpg
│   │   │   │   ├── menu-items.zip
│   │   │   │   ├── menudo-sat-and-sun-only.jpg
│   │   │   │   ├── michelob-ultra-light-usa-limited-edition-beer-slim-cans-(12-fl-oz-x-24-ct).jpg
│   │   │   │   ├── modelo-especial-mexican-lager-bottles-(12-fl-oz-x-12-ct).jpg
│   │   │   │   ├── nachos-supreme.jpg
│   │   │   │   ├── party-packs.jpg
│   │   │   │   ├── pollo-asada-quesadilla.jpg
│   │   │   │   ├── pollo-asado-burrito.jpg
│   │   │   │   ├── pollo-asado-taco.jpg
│   │   │   │   ├── pollo-asado-torta.jpg
│   │   │   │   ├── protein-bowl.jpg
│   │   │   │   ├── protein-fries.jpg
│   │   │   │   ├── quesadillas.jpg
│   │   │   │   ├── rice-(8-oz).jpg
│   │   │   │   ├── rolled-tacos-(50).jpg
│   │   │   │   ├── rolled-with-guacamole-(3).jpg
│   │   │   │   ├── rolled-with-guacamole-(5).jpg
│   │   │   │   ├── rolled-with-sour-cream-(3).jpg
│   │   │   │   ├── rolled-with-sour-cream-(5).jpg
│   │   │   │   ├── shredded-beef-taco.jpg
│   │   │   │   ├── shredded-chicken-quesadilla.jpg
│   │   │   │   ├── shredded-chicken-taco.jpg
│   │   │   │   ├── shrimp-burrito.jpg
│   │   │   │   ├── shrimp-fries.jpg
│   │   │   │   ├── shrimp-quesadilla.jpg
│   │   │   │   ├── shrimp-taco.jpg
│   │   │   │   ├── side-of-rice-serves-20.jpg
│   │   │   │   ├── side-orders.jpg
│   │   │   │   ├── soon.jpg
│   │   │   │   ├── steak-and-eggs-burrito.jpg
│   │   │   │   ├── super-breakfast-bowl.jpg
│   │   │   │   ├── super-breakfast-burrito.jpg
│   │   │   │   ├── supreme-burrito.jpg
│   │   │   │   ├── surf-and-turf-bowl.jpg
│   │   │   │   ├── surf-and-turf-fries.jpg
│   │   │   │   ├── surf-n'-turf-burrito.jpg
│   │   │   │   ├── tacos---hard.jpg
│   │   │   │   ├── tacos---soft.jpg
│   │   │   │   ├── taquito-burrito.jpg
│   │   │   │   ├── tito's-gluten-free-80-proof-handmade-vodka-bottle-(750-ml).jpg
│   │   │   │   ├── two4tentacos.jpg
│   │   │   │   ├── veggie-fries.jpg
│   │   │   │   ├── veggie-quesadilla.jpg
│   │   │   │   └── white-claw-gluten-free-no.-1-variety-pack-hard-seltzer-cans-(12-fl-oz-x-12-ct).jpg
│   │   │   ├── new-bun.jpg
│   │   │   ├── reservation.jpg
│   │   │   ├── stats-bg.jpg
│   │   │   ├── taco.png
│   │   │   ├── tacos-front.webp
│   │   │   ├── tacos.webp
│   │   │   ├── team-shape.svg
│   │   │   └── testimonials
│   │   │       ├── testimonials-1.jpg
│   │   │       ├── testimonials-2.jpg
│   │   │       ├── testimonials-3.jpg
│   │   │       └── testimonials-4.jpg
│   │   ├── js
│   │   │   ├── main.js
│   │   │   └── reviews.js
│   │   ├── scss
│   │   └── vendor
│   │       ├── aos
│   │       │   ├── aos.cjs.js
│   │       │   ├── aos.css
│   │       │   ├── aos.esm.js
│   │       │   ├── aos.js
│   │       │   └── aos.js.map
│   │       ├── bootstrap
│   │       │   ├── css
│   │       │   │   ├── bootstrap-grid.css
│   │       │   │   ├── bootstrap-grid.css.map
│   │       │   │   ├── bootstrap-grid.min.css
│   │       │   │   ├── bootstrap-grid.min.css.map
│   │       │   │   ├── bootstrap-grid.rtl.css
│   │       │   │   ├── bootstrap-grid.rtl.css.map
│   │       │   │   ├── bootstrap-grid.rtl.min.css
│   │       │   │   ├── bootstrap-grid.rtl.min.css.map
│   │       │   │   ├── bootstrap-reboot.css
│   │       │   │   ├── bootstrap-reboot.css.map
│   │       │   │   ├── bootstrap-reboot.min.css
│   │       │   │   ├── bootstrap-reboot.min.css.map
│   │       │   │   ├── bootstrap-reboot.rtl.css
│   │       │   │   ├── bootstrap-reboot.rtl.css.map
│   │       │   │   ├── bootstrap-reboot.rtl.min.css
│   │       │   │   ├── bootstrap-reboot.rtl.min.css.map
│   │       │   │   ├── bootstrap-utilities.css
│   │       │   │   ├── bootstrap-utilities.css.map
│   │       │   │   ├── bootstrap-utilities.min.css
│   │       │   │   ├── bootstrap-utilities.min.css.map
│   │       │   │   ├── bootstrap-utilities.rtl.css
│   │       │   │   ├── bootstrap-utilities.rtl.css.map
│   │       │   │   ├── bootstrap-utilities.rtl.min.css
│   │       │   │   ├── bootstrap-utilities.rtl.min.css.map
│   │       │   │   ├── bootstrap.css
│   │       │   │   ├── bootstrap.css.map
│   │       │   │   ├── bootstrap.min.css
│   │       │   │   ├── bootstrap.min.css.map
│   │       │   │   ├── bootstrap.rtl.css
│   │       │   │   ├── bootstrap.rtl.css.map
│   │       │   │   ├── bootstrap.rtl.min.css
│   │       │   │   ├── bootstrap.rtl.min.css.map
│   │       │   │   └── prb.txt
│   │       │   └── js
│   │       │       ├── bootstrap.bundle.js
│   │       │       ├── bootstrap.bundle.js.map
│   │       │       ├── bootstrap.bundle.min.js
│   │       │       ├── bootstrap.bundle.min.js.map
│   │       │       ├── bootstrap.esm.js
│   │       │       ├── bootstrap.esm.js.map
│   │       │       ├── bootstrap.esm.min.js
│   │       │       ├── bootstrap.esm.min.js.map
│   │       │       ├── bootstrap.js
│   │       │       ├── bootstrap.js.map
│   │       │       ├── bootstrap.min.js
│   │       │       └── bootstrap.min.js.map
│   │       ├── bootstrap-icons
│   │       │   ├── bootstrap-icons.css
│   │       │   ├── bootstrap-icons.json
│   │       │   ├── bootstrap-icons.min.css
│   │       │   ├── bootstrap-icons.scss
│   │       │   └── fonts
│   │       │       ├── bootstrap-icons.woff
│   │       │       └── bootstrap-icons.woff2
│   │       ├── glightbox
│   │       │   ├── css
│   │       │   │   ├── glightbox.css
│   │       │   │   └── glightbox.min.css
│   │       │   └── js
│   │       │       ├── glightbox.js
│   │       │       └── glightbox.min.js
│   │       ├── php-email-form
│   │       │   └── validate.js
│   │       ├── purecounter
│   │       │   ├── purecounter_vanilla.js
│   │       │   └── purecounter_vanilla.js.map
│   │       └── swiper
│   │           ├── swiper-bundle.min.css
│   │           ├── swiper-bundle.min.js
│   │           └── swiper-bundle.min.js.map
│   ├── index.html
│   ├── latest-news.html
│   ├── locations.html
│   ├── menu.html
│   ├── posts
│   │   ├── anatomy-fish-taco
│   │   │   └── index.html
│   │   ├── breakfast-burritos
│   │   │   └── index.html
│   │   ├── bunuelos-crispy-sweet-treat
│   │   │   └── index.html
│   │   ├── fresh-and-authentic
│   │   │   └── index.html
│   │   ├── two-for-ten
│   │   │   └── index.html
│   │   └── voted-top-ten-yelp
│   │       └── index.html
│   └── test.html
├── file-tree.py
├── file_tree.txt
├── firebase.json
├── functions
│   ├── index.js
│   ├── package-lock.json
│   └── package.json
├── github-poller
│   ├── app.py
│   ├── index.html
│   └── requirements.txt
├── notes
├── notes.md
├── package-lock.json
├── package.json
├── rev.json
└── src
    ├── _includes
    │   ├── footer.njk
    │   └── header.njk
    ├── _layouts
    │   └── base.njk
    ├── assets
    │   ├── css
    │   │   ├── custom.css
    │   │   ├── main.css
    │   │   └── vendor.min.css
    │   ├── img
    │   │   ├── about-2.jpg
    │   │   ├── about.jpg
    │   │   ├── apple-touch-icon.png
    │   │   ├── blog
    │   │   │   ├── bunuelos.jpg
    │   │   │   ├── dinner-plate.jpg
    │   │   │   └── dinner.jpg
    │   │   ├── carne-asada.png
    │   │   ├── carneasada plate.png
    │   │   ├── chefs
    │   │   │   ├── chefs-1.jpg
    │   │   │   ├── chefs-2.jpg
    │   │   │   └── chefs-3.jpg
    │   │   ├── el-pueblo-logo.png
    │   │   ├── el_pueblo_mex_logo-01.png
    │   │   ├── events-1.jpg
    │   │   ├── events-2.jpg
    │   │   ├── events-3.jpg
    │   │   ├── events-4.jpg
    │   │   ├── favicon.png
    │   │   ├── gallery
    │   │   │   ├── gallery-1.jpg
    │   │   │   ├── gallery-2.jpg
    │   │   │   ├── gallery-3.jpg
    │   │   │   ├── gallery-4.jpg
    │   │   │   ├── gallery-5.jpg
    │   │   │   ├── gallery-6.jpg
    │   │   │   ├── gallery-7.jpg
    │   │   │   └── gallery-8.jpg
    │   │   ├── hero-img.png
    │   │   ├── logo.png
    │   │   ├── menu
    │   │   │   ├── menu-item-1.png
    │   │   │   ├── menu-item-2.png
    │   │   │   ├── menu-item-3.png
    │   │   │   ├── menu-item-4.png
    │   │   │   ├── menu-item-5.png
    │   │   │   └── menu-item-6.png
    │   │   ├── menu-items
    │   │   │   ├── 2-for-10-taco-combo.jpg
    │   │   │   ├── adobada-burrito.jpg
    │   │   │   ├── adobada-quesadilla.jpg
    │   │   │   ├── adobada-taco.jpg
    │   │   │   ├── adobada-torta.jpg
    │   │   │   ├── bean-and-cheese-burrito.jpg
    │   │   │   ├── breakfast-bowl.jpg
    │   │   │   ├── breakfast-burrito.jpg
    │   │   │   ├── breakfast.jpg
    │   │   │   ├── cali-burrito.jpg
    │   │   │   ├── carne-asada-burrito.jpg
    │   │   │   ├── carne-asada-plate.jpg
    │   │   │   ├── carne-asada-quesadilla.jpg
    │   │   │   ├── carne-asada-taco.jpg
    │   │   │   ├── carne-asada-torta.jpg
    │   │   │   ├── carnitas-burrito.jpg
    │   │   │   ├── carnitas-burrito2.jpg
    │   │   │   ├── carnitas-plate.jpg
    │   │   │   ├── carnitas-quesadilla.jpg
    │   │   │   ├── carnitas-taco.jpg
    │   │   │   ├── carnitas-torta.jpg
    │   │   │   ├── cheese-quesadilla.jpg
    │   │   │   ├── chickentortsoup.jpg
    │   │   │   ├── chilaquiles-rojos.jpg
    │   │   │   ├── chilaquiles-verdes.jpg
    │   │   │   ├── chile-relleno-burrito.jpg
    │   │   │   ├── chile-relleno-plate.jpg
    │   │   │   ├── chile-relleno.jpg
    │   │   │   ├── chimichanga.jpg
    │   │   │   ├── chips-and-salsa.jpg
    │   │   │   ├── chorizo-burrito.jpg
    │   │   │   ├── chorizo-plate.jpg
    │   │   │   ├── chorizo-torta.jpg
    │   │   │   ├── conga-burrito.jpg
    │   │   │   ├── dinners.jpg
    │   │   │   ├── el-pueblo-mexican-food.jpg
    │   │   │   ├── el-pueblo-torta-with-fries.jpg
    │   │   │   ├── enchiladas.jpg
    │   │   │   ├── fajitas-burrito.jpg
    │   │   │   ├── fajitas-plate.jpg
    │   │   │   ├── fish-taco.jpg
    │   │   │   ├── fish_tacos.jpg
    │   │   │   ├── flautas-(3).jpg
    │   │   │   ├── fries-and-chips.jpg
    │   │   │   ├── full-menu.jpg
    │   │   │   ├── guacamole-(1-2-tray).jpg
    │   │   │   ├── ham-and-cheese.jpg
    │   │   │   ├── huevos-a-la-mexicana.jpg
    │   │   │   ├── huevos-con-jamon.jpg
    │   │   │   ├── huevos-rancheros.jpg
    │   │   │   ├── josh-cellars-vintage-pinot-noir-bottle-central-coast-(750-ml).jpg
    │   │   │   ├── kids-quesadilla.jpg
    │   │   │   ├── la-marca-prosecco-bottle-doc-italy-(375-ml).jpg
    │   │   │   ├── lengua-taco.jpg
    │   │   │   ├── machaca-burrito.jpg
    │   │   │   ├── machaca-plate.jpg
    │   │   │   ├── machaca-torta.jpg
    │   │   │   ├── make-your-own-tacos.jpg
    │   │   │   ├── menu-items.zip
    │   │   │   ├── menudo-sat-and-sun-only.jpg
    │   │   │   ├── michelob-ultra-light-usa-limited-edition-beer-slim-cans-(12-fl-oz-x-24-ct).jpg
    │   │   │   ├── modelo-especial-mexican-lager-bottles-(12-fl-oz-x-12-ct).jpg
    │   │   │   ├── nachos-supreme.jpg
    │   │   │   ├── party-packs.jpg
    │   │   │   ├── pollo-asada-quesadilla.jpg
    │   │   │   ├── pollo-asado-burrito.jpg
    │   │   │   ├── pollo-asado-taco.jpg
    │   │   │   ├── pollo-asado-torta.jpg
    │   │   │   ├── protein-bowl.jpg
    │   │   │   ├── protein-fries.jpg
    │   │   │   ├── quesadillas.jpg
    │   │   │   ├── rice-(8-oz).jpg
    │   │   │   ├── rolled-tacos-(50).jpg
    │   │   │   ├── rolled-with-guacamole-(3).jpg
    │   │   │   ├── rolled-with-guacamole-(5).jpg
    │   │   │   ├── rolled-with-sour-cream-(3).jpg
    │   │   │   ├── rolled-with-sour-cream-(5).jpg
    │   │   │   ├── shredded-beef-taco.jpg
    │   │   │   ├── shredded-chicken-quesadilla.jpg
    │   │   │   ├── shredded-chicken-taco.jpg
    │   │   │   ├── shrimp-burrito.jpg
    │   │   │   ├── shrimp-fries.jpg
    │   │   │   ├── shrimp-quesadilla.jpg
    │   │   │   ├── shrimp-taco.jpg
    │   │   │   ├── side-of-rice-serves-20.jpg
    │   │   │   ├── side-orders.jpg
    │   │   │   ├── soon.jpg
    │   │   │   ├── steak-and-eggs-burrito.jpg
    │   │   │   ├── super-breakfast-bowl.jpg
    │   │   │   ├── super-breakfast-burrito.jpg
    │   │   │   ├── supreme-burrito.jpg
    │   │   │   ├── surf-and-turf-bowl.jpg
    │   │   │   ├── surf-and-turf-fries.jpg
    │   │   │   ├── surf-n'-turf-burrito.jpg
    │   │   │   ├── tacos---hard.jpg
    │   │   │   ├── tacos---soft.jpg
    │   │   │   ├── taquito-burrito.jpg
    │   │   │   ├── tito's-gluten-free-80-proof-handmade-vodka-bottle-(750-ml).jpg
    │   │   │   ├── two4tentacos.jpg
    │   │   │   ├── veggie-fries.jpg
    │   │   │   ├── veggie-quesadilla.jpg
    │   │   │   └── white-claw-gluten-free-no.-1-variety-pack-hard-seltzer-cans-(12-fl-oz-x-12-ct).jpg
    │   │   ├── new-bun.jpg
    │   │   ├── reservation.jpg
    │   │   ├── stats-bg.jpg
    │   │   ├── taco.png
    │   │   ├── tacos-front.webp
    │   │   ├── tacos.webp
    │   │   ├── team-shape.svg
    │   │   └── testimonials
    │   │       ├── testimonials-1.jpg
    │   │       ├── testimonials-2.jpg
    │   │       ├── testimonials-3.jpg
    │   │       └── testimonials-4.jpg
    │   ├── js
    │   │   ├── main.js
    │   │   └── reviews.js
    │   ├── scss
    │   └── vendor
    │       ├── aos
    │       │   ├── aos.cjs.js
    │       │   ├── aos.css
    │       │   ├── aos.esm.js
    │       │   ├── aos.js
    │       │   └── aos.js.map
    │       ├── bootstrap
    │       │   ├── css
    │       │   │   ├── bootstrap-grid.css
    │       │   │   ├── bootstrap-grid.css.map
    │       │   │   ├── bootstrap-grid.min.css
    │       │   │   ├── bootstrap-grid.min.css.map
    │       │   │   ├── bootstrap-grid.rtl.css
    │       │   │   ├── bootstrap-grid.rtl.css.map
    │       │   │   ├── bootstrap-grid.rtl.min.css
    │       │   │   ├── bootstrap-grid.rtl.min.css.map
    │       │   │   ├── bootstrap-reboot.css
    │       │   │   ├── bootstrap-reboot.css.map
    │       │   │   ├── bootstrap-reboot.min.css
    │       │   │   ├── bootstrap-reboot.min.css.map
    │       │   │   ├── bootstrap-reboot.rtl.css
    │       │   │   ├── bootstrap-reboot.rtl.css.map
    │       │   │   ├── bootstrap-reboot.rtl.min.css
    │       │   │   ├── bootstrap-reboot.rtl.min.css.map
    │       │   │   ├── bootstrap-utilities.css
    │       │   │   ├── bootstrap-utilities.css.map
    │       │   │   ├── bootstrap-utilities.min.css
    │       │   │   ├── bootstrap-utilities.min.css.map
    │       │   │   ├── bootstrap-utilities.rtl.css
    │       │   │   ├── bootstrap-utilities.rtl.css.map
    │       │   │   ├── bootstrap-utilities.rtl.min.css
    │       │   │   ├── bootstrap-utilities.rtl.min.css.map
    │       │   │   ├── bootstrap.css
    │       │   │   ├── bootstrap.css.map
    │       │   │   ├── bootstrap.min.css
    │       │   │   ├── bootstrap.min.css.map
    │       │   │   ├── bootstrap.rtl.css
    │       │   │   ├── bootstrap.rtl.css.map
    │       │   │   ├── bootstrap.rtl.min.css
    │       │   │   ├── bootstrap.rtl.min.css.map
    │       │   │   └── prb.txt
    │       │   └── js
    │       │       ├── bootstrap.bundle.js
    │       │       ├── bootstrap.bundle.js.map
    │       │       ├── bootstrap.bundle.min.js
    │       │       ├── bootstrap.bundle.min.js.map
    │       │       ├── bootstrap.esm.js
    │       │       ├── bootstrap.esm.js.map
    │       │       ├── bootstrap.esm.min.js
    │       │       ├── bootstrap.esm.min.js.map
    │       │       ├── bootstrap.js
    │       │       ├── bootstrap.js.map
    │       │       ├── bootstrap.min.js
    │       │       └── bootstrap.min.js.map
    │       ├── bootstrap-icons
    │       │   ├── bootstrap-icons.css
    │       │   ├── bootstrap-icons.json
    │       │   ├── bootstrap-icons.min.css
    │       │   ├── bootstrap-icons.scss
    │       │   └── fonts
    │       │       ├── bootstrap-icons.woff
    │       │       └── bootstrap-icons.woff2
    │       ├── glightbox
    │       │   ├── css
    │       │   │   ├── glightbox.css
    │       │   │   └── glightbox.min.css
    │       │   └── js
    │       │       ├── glightbox.js
    │       │       └── glightbox.min.js
    │       ├── php-email-form
    │       │   └── validate.js
    │       ├── purecounter
    │       │   ├── purecounter_vanilla.js
    │       │   └── purecounter_vanilla.js.map
    │       └── swiper
    │           ├── swiper-bundle.min.css
    │           ├── swiper-bundle.min.js
    │           └── swiper-bundle.min.js.map
    ├── blog.njk
    ├── index.njk
    ├── locations.njk
    ├── menu.njk
    ├── posts
    │   ├── anatomy-fish-taco.md
    │   ├── breakfast-burritos.md
    │   ├── bunuelos-crispy-sweet-treat.md
    │   ├── freash-and-authentic.md
    │   ├── two-for-ten.md
    │   └── yelp-voted-top-ten.md
    ├── robots.txt
    └── test.njk

---

 April 2, 2025 

 🧠 Goal
You wanted to display recent blog post previews on your Eleventy-powered homepage (index.njk) and encountered issues with collections and layout.

✅ What We Diagnosed and Solved
1. Blog Posts Not Showing on Homepage
Your blog posts were correctly tagged and visible on the blog listing page.

However, they were not rendering on the homepage.

We confirmed collections.blog had 6 posts, but collections.blogLatest returned 0.

2. Issue with slice() in .eleventy.js
Using .slice(0, 3) directly in a custom collection (blogLatest) caused it to return an empty array due to build timing issues.

Fix: Instead of slicing in .eleventy.js, we now slice inside the template using:

njk
Copy
Edit
{% set blogLatest = collections.blog.slice(0, 3) %}
3. Rendering Fix
Updated the index.njk to:

Use collections.blog.slice(0, 3)

Render Bootstrap card layout like your latest-news.njk template

Fixed layout bugs and ensured visibility

4. HTML Cleanup
Resolved an invalid {# ... #} Nunjucks comment block that caused HTML parsing errors

Ensured all tags in your homepage template were correctly opened and closed

5. Updated .eleventy.js
Cleaned it up to include:

blog collection only (no need for blogLatest)

Luxon-based date filter

Passthrough copy for assets

Correct directory configuration

✅ Final State
✅ Blog posts show on homepage via collections.blog.slice(0, 3)

✅ No Eleventy build errors

✅ Clean and maintainable index.njk and .eleventy.js

---
 Absolutely. Here's a **text-only summary** of everything we've covered in this conversation so far:

---

### 🧱 **Project Setup & Goals**
- You’re building a static site with **Eleventy (11ty)** and deploying via **Firebase Hosting**.
- You wanted a **fully customizable contact form** that integrates with your site.
- We explored whether to use **Firebase Functions** or a **Flask API with Cloud Run** — you chose Flask on Cloud Run for flexibility.

---

### ⚙️ **Flask + Cloud Run Setup**
1. Created a `contact-form-api/` directory with `app.py`, `requirements.txt`, and a `Dockerfile`.
2. Flask app included a `/submit` endpoint that receives form data via POST.
3. Docker image was built and deployed to **Google Cloud Run** using:
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/contact-form
   gcloud run deploy contact-form --image gcr.io/PROJECT_ID/contact-form --platform managed --region us-central1 --allow-unauthenticated
   ```
4. Eleventy site submits the form via `fetch()` to the live Cloud Run endpoint.

---

### 🚨 **CORS Issue & Fix**
- You hit a CORS error when testing the form.
- Solution: Installed `flask-cors` and added:
  ```python
  CORS(app, origins="*", methods=["GET", "POST", "OPTIONS"])
  ```
- Also handled `OPTIONS` requests explicitly in the Flask route.

---

### 📬 **Sending Emails via Gmail**
- Created a Gmail **App Password** for `it@elpueblomex.com`
- Updated Flask to send email via `smtplib` using:
  ```python
  smtp.login(GMAIL_USER, GMAIL_PASSWORD)
  smtp.send_message(msg)
  ```
- Emails now arrive successfully in the inbox.

---

### 📊 **Logging Submissions to Google Sheets (in progress)**
- Created a Google Sheet with headers: `Timestamp | Name | Email | Message`
- Set up a **Service Account** with access to Google Sheets API
- Shared the sheet with the service account
- Downloaded the JSON credentials file
- Preparing to use `gspread` or `google-api-python-client` to log submissions from Flask

---

Let me know if you want this saved or exported as a `.txt` or markdown file. When you’re ready, type **`next`** to continue integrating Google Sheets.


⚙️ Environment
Project: yummy-elpueblo-11ty

Backend: contact-form-api

Serving With: Flask + Gunicorn

Docker Registry: Artifact Registry (NOT GCR)

Deployment Target: Cloud Run (upbeat-button-265722)

Local Dev: WSL + PowerShell mix

Email Destinations: rob@elpueblomex.com, rob@barbank.com

✅ Command Style
Always inline, even if multi-line

No backslashes \

PowerShell by default if unspecified, otherwise WSL when running inside Linux shell