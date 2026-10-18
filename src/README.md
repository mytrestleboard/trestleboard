# How the site is built

- `index.html` is GENERATED. Do not edit it by hand; your change will be lost on the next build.
- Edit `src/template.html` (the whole app: HTML, CSS, JS) and the data files in `src/data/`.
- Build: `python3 src/build_public.py` from the repo root, then `node --check .build-check.js`, then commit `src/` and `index.html` together.
- The public build has no officer names, Monitor, drills or law book. Those live in Supabase (`docs` table: coll `offpre` id `_`, coll `ref` ids `mon`, `drills`, `laws`) and load for signed-in verified members. `src/data/stubs.json` holds the empty shells the template expects.
- Supabase project: njoxlxwhkhkdyqkckfji. Edge function `verify-card` source is kept in the project docs (claude/verify-card-resolved.md).
- Other files in the repo root (manifest, icons, sw.js, CNAME) are hand-maintained and not touched by the build.
