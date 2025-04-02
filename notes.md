# 📘 Eleventeenth Project Context — `elpueblo-11ty`

## 🧠 Project Purpose

This is a content-rich static site built with [11ty (Eleventy)](https://11ty.dev). It integrates:
- Custom GitHub polling logic via Python
- Firebase Hosting + optional Cloud Functions
- Custom templates and layouts for content like locations, menus, and blog-style posts

The project uses a structured source folder and a Python-based data fetcher to pull GitHub info into Eleventy templates dynamically.

---

## 📁 Directory Structure Overview

```
elpueblo-11ty/
├── .eleventy.js          → Eleventy config file
├── src/                  → Main 11ty input folder
│   ├── _includes/        → Nunjucks partials
│   ├── _layouts/         → Base templates/layouts
│   ├── posts/            → Markdown or template content (TBD)
│   ├── blog.njk          → Blog listing template
│   ├── index.njk         → Main landing page
│   ├── locations.njk     → Location content
│   ├── menu.njk          → Structured menu or content map (large)
│   ├── test.njk          → Test template
│   └── _data/github.json → Auto-generated GitHub data
│
├── github-poller/        → Python app that fetches GitHub commits
│   ├── app.py            → Polls GitHub API and writes to _data
│   ├── requirements.txt  → Contains `requests`
│   └── index.html        → Optional output interface
│
├── functions/            → Firebase functions (not yet reviewed)
├── design-source/        → Likely raw design assets
├── code-pull-index.html  → Large generated or static HTML file
├── file-tree.py          → Generates file tree (internal use)
├── file_tree.txt         → Output of file-tree.py
├── firebase.json         → Firebase hosting config
├── .firebaserc           → Firebase project settings
├── rev.json              → Possibly a build rev marker
├── notes                 → Small file, maybe placeholder
├── package.json          → Contains scripts + Eleventy dep
└── READ.MD               → Rename to README.md
```

---

## 🔄 GitHub Poller Integration

- `github-poller/app.py` fetches recent commits from GitHub
- Output is written to `src/_data/github.json`
- This makes commit data available in any 11ty template as `github`

🧪 Sample Nunjucks usage:
```njk
{% for commit in github %}
  <p>{{ commit.commit.message }} — {{ commit.commit.author.date }}</p>
{% endfor %}
```

🛠️ Enhancements coming soon:
- Filtering commit data
- Auto-deployment via GitHub Actions or Firebase Functions
- Schedule-based polling or webhook triggers

---

## ✅ Setup Tasks

- [ ] Confirm `posts/` content structure
- [ ] Review and optimize `.eleventy.js` for collections and passthroughs
- [ ] Clean up loose files (`rev.json`, `notes`, `READ.MD`)
- [ ] Break up or modularize `menu.njk` (~46 KB)
- [ ] Add GitHub token support to `app.py` (via `.env` or secrets manager)
- [ ] Add cron job or Firebase Function to automate poller

---

