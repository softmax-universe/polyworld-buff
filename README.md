# Polyworld Buff

Public game documentation hosted on GitHub Pages.

- [Home](https://softmax-universe.github.io/polyworld-buff/)
- [Gods of the Arena](https://softmax-universe.github.io/polyworld-buff/GOTA/)
- [Light vs Dark](https://softmax-universe.github.io/polyworld-buff/LvD/)
- [Call to Adventure](https://softmax-universe.github.io/polyworld-buff/CTA/)

Each game folder contains an `index.html` and the images and fonts it uses in
`assets/`. The pages are copied from the corresponding game documentation in
`polyworld/examples/`, with asset paths updated for this repository.

GitHub Pages publishes the repository root from the `main` branch. Pushing
changes to `main` updates the public site. No build step is needed. The
`.nojekyll` file tells GitHub Pages to serve the static files directly.

To preview locally, run `python3 -m http.server 8000` from this directory and
open [the local site](http://localhost:8000/).
