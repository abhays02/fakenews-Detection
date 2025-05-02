// Handles UI, feedback, and receives prediction from background script
const confidenceEl = document.getElementById('confidence');
const messageEl = document.getElementById('message');
const resultEl = messageEl.querySelector('.result');
const feedbackBtn = document.getElementById('feedback-btn');
const feedbackForm = document.getElementById('feedback-form');
const submitFeedback = document.getElementById('submit-feedback');
const feedbackText = document.getElementById('feedback-text');
const aboutAI = document.getElementById('about-ai');

// Listen for prediction result from background
chrome.runtime.sendMessage({ action: 'getPrediction' }, (response) => {
  if (response && response.prediction !== undefined) {
    const { prediction, confidence } = response;
    const isReal = prediction === 0;
    confidenceEl.textContent = `${isReal ? '🔵' : '🔴'} ${Math.round(confidence * 100)}% ${isReal ? 'Real' : 'Fake'}`;
    resultEl.textContent = isReal ? 'Real' : 'Fake';
    resultEl.className = 'result ' + (isReal ? 'real' : 'fake');
    messageEl.innerHTML = `This article seems <span class='result ${isReal ? 'real' : 'fake'}'>${isReal ? 'Real' : 'Fake'}</span> based on AI analysis.`;
  } else {
    confidenceEl.textContent = 'No article detected';
    messageEl.textContent = '';
  }
});

feedbackBtn.onclick = () => {
  feedbackForm.classList.remove('hidden');
};
submitFeedback.onclick = () => {
  // Send feedback to background or a server
  chrome.runtime.sendMessage({ action: 'submitFeedback', text: feedbackText.value });
  feedbackForm.classList.add('hidden');
  feedbackText.value = '';
  alert('Thank you for your feedback!');
};
aboutAI.onclick = () => {
  window.open('https://huggingface.co/bert-base-uncased', '_blank');
};
