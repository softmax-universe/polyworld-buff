'use strict';

const copyPromptButton = document.querySelector('.copy-prompt');
const gnomePrompt = document.getElementById('gnome-prompt');
const promptStatus = document.querySelector('.prompt-status');

copyPromptButton.addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(gnomePrompt.textContent);
    copyPromptButton.textContent = 'Copied';
    promptStatus.textContent = 'Prompt copied to clipboard.';
  } catch {
    promptStatus.textContent = 'Select the prompt text to copy it.';
  }
});
