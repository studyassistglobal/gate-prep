# GATE Prep

Free chapter-wise study notes for **GATE 2027 (ECE)** — deep, faculty-style theory with worked solutions, faculty traps and exam strategy. Public site: no login, no paywall.

Live: **https://gate-prep.pages.dev** (project `gate-prep` on Cloudflare Pages)

## What's inside

- **Digital Electronics** — Ch 1: Logic Gates & Boolean Algebra · Ch 2: Boolean Expressions & K-Maps · Ch 3: Number Systems & Digital Representation · Ch 4 Parts 1–2: Combinational Circuits
- 73 sections / 2,400+ content blocks rendered from the Master Guide markdown sources, with KaTeX math, figures, alert callouts and collapsible worked solutions
- Reading progress per section (localStorage, no account), course/section search, light & dark theme

## Architecture

React 18 + Vite 5 (HashRouter), forked from the ExamPrep Hub codebase with all auth/Supabase/exam machinery stripped. Content is **generated, never hand-edited**:

```
D:/GATE 2027/Digital electronics/*_Master_Guide.md
        │  scripts/build_notes.py
        ▼
src/data/notes/de/ch1.js, ch2.js   (typed block AST: p/h3/h4/ul/ol/table/code/alert/details/img/math)
src/data/notes/de/index.js         (lightweight section index for accordion + search)
public/notes/de/figures*/          (chapter figures — PNG for ch1/ch2, JPG for ch3)
```

`src/data/courses.js` is the registry — new chapters/subjects are a registry entry + a generated module.

## Commands

```bash
npm run dev            # dev server on :5175
npm run build:notes    # regenerate note modules from the Master Guide MDs
npm run verify         # scripts/verify_notes.mjs — registry/AST/figure/search/fork-hygiene checks
npm run build          # production build (rm -rf dist first if chunks look stale — emptyOutDir is false)
npx wrangler pages deploy dist --project-name=gate-prep
```

## Invariants

- Never edit `src/data/notes/**` by hand — edit the Master Guide MD, then rerun `npm run build:notes`.
- Run `npm run verify` + `npm run build` before every deploy.
- The site is fully public: do not reintroduce auth/Supabase without a plan (localStorage keys: `gp_progress_v1`, `df-theme`).
