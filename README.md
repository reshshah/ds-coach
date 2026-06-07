# Applied AI Director Coach

A personal AI-powered coaching hub to prepare for Director, Data Science roles on Applied AI teams — specifically targeting Walmart Global Tech's Applied AI team.

**Live site:** https://ds-coach-dusky.vercel.app/

---

## What's Inside

| Tab | What it does |
|-----|-------------|
| **Home** | Dashboard with progress tracking across both tools |
| **30-Day Plan** | Daily 1hr coaching sessions covering forecasting, agentic AI, gen AI, MLOps, optimization, leadership, and mock interviews |
| **Interview Questions** | 8 Director-level questions (Walmart, Google, Amazon) with scored critiques |
| **Target Role** | Full job description and requirements breakdown for Walmart Applied AI Director role |

---

## Accessing the Site

**URL:** https://ds-coach-dusky.vercel.app/

**PIN:** stored locally — check `index.html` for `APP_PIN` variable if you forget it.

**Add to phone home screen:**
- iPhone: Open URL in Safari → Share → Add to Home Screen
- Android: Open URL in Chrome → menu → Add to Home Screen

---

## How It Works

```
Browser → Vercel serverless function (api/proxy.js) → Anthropic API
```

- The Anthropic API key lives as a **Vercel environment variable** — never in the code
- The PIN lock prevents unauthorized use
- Progress is saved in browser `localStorage` — persists across visits on the same device

---

## Repo Structure

```
ds-coach/
├── index.html          # Full single-page app (all 4 tabs)
├── api/
│   └── proxy.js        # Vercel serverless function — proxies Anthropic API calls
├── vercel.json         # Vercel config — routing and output directory
└── README.md           # This file
```

---

## Making Changes

### Edit the coaching content
All content lives in `index.html`:
- **30-day plan topics** → find `var WEEKS = [...]`
- **Interview questions** → find `var QUESTIONS = [...]`
- **Coaching system prompt** → find `var PLAN_SYSTEM = '...'`
- **Target role details** → find `<!-- TARGET ROLE -->` in the HTML
- **PIN** → find `var APP_PIN = '...'`

### Deploy changes
1. Edit files in the repo on GitHub (pencil icon) or locally
2. Commit to `main` branch
3. Vercel auto-deploys within ~30 seconds — no manual steps needed

### Update the API key
1. Go to [vercel.com](https://vercel.com) → your project → **Settings → Environment Variables**
2. Find `ANTHROPIC_API_KEY` → edit the value
3. Redeploy (Vercel dashboard → Deployments → Redeploy)

### Add a new interview question
Find `var QUESTIONS = [...]` in `index.html` and add a new object following this pattern:
```javascript
{
  id: 9,
  type: 'ml',           // ml, behavioral, or strategy
  company: 'Walmart',
  title: 'Your question title',
  question: 'Full question text here.',
  hints: [
    'Hint 1',
    'Hint 2',
    'Hint 3',
    'Hint 4'
  ],
  done: false
}
```

### Add a new coaching day
Find `var WEEKS = [...]` and add to the relevant week's `days` array:
```javascript
{day: 31, topic: 'New Topic', icon: '🎯', summary: 'What this session covers'}
```

---

## Vercel Setup (for reference)

If you ever need to redeploy from scratch:

1. Go to [vercel.com](https://vercel.com) → Add New Project → Import `reshshah/ds-coach`
2. Framework: **Other**
3. Output Directory: `ds-coach`
4. Environment Variables: add `ANTHROPIC_API_KEY` = your `sk-ant-...` key
5. Click Deploy

---

## Tech Stack

- **Frontend:** Vanilla HTML/CSS/JS — no build step, no dependencies
- **AI:** Anthropic Claude Sonnet (`claude-sonnet-4-20250514`)
- **Hosting:** Vercel (free tier)
- **API proxy:** Vercel serverless function (Node.js)
- **Storage:** Browser localStorage for progress tracking

---

## Security Notes

- API key is stored as a Vercel environment variable — never in the codebase
- PIN lock prevents unauthorized access to the live site
- Do **not** add the API key directly to `index.html` — use Vercel env vars only
- If you suspect the key is compromised, rotate it at [console.anthropic.com](https://console.anthropic.com) and update the Vercel env var

---

*Built with Claude · Targeting Walmart Applied AI Director · 30 days · 1hr/day*
