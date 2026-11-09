'use strict';

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const clips = [...document.querySelectorAll('.shot video')];
const states = new Map();

for (const clip of clips) {
  const state = {visible: false, pausedByUser: false};
  states.set(clip, state);
  clip.muted = true;
  clip.addEventListener('pause', () => {
    if (state.visible && !reducedMotion.matches) state.pausedByUser = true;
  });
  clip.addEventListener('play', () => { state.pausedByUser = false; });
}

const observer = new IntersectionObserver(entries => {
  for (const entry of entries) {
    const clip = entry.target;
    const state = states.get(clip);
    state.visible = entry.isIntersecting;
    if (state.visible && !reducedMotion.matches && !state.pausedByUser) {
      clip.play().catch(() => {});
    } else if (!state.visible) {
      clip.pause();
    }
  }
}, {threshold: 0.2});

for (const clip of clips) observer.observe(clip);

reducedMotion.addEventListener('change', () => {
  for (const clip of clips) {
    const state = states.get(clip);
    if (reducedMotion.matches) clip.pause();
    else if (state.visible && !state.pausedByUser) clip.play().catch(() => {});
  }
});
