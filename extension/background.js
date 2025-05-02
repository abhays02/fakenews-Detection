// Loads prediction from FastAPI backend, manages badge and messaging
let lastPrediction = { prediction: undefined, confidence: 0 };

async function predict(text) {
  try {
    const response = await fetch('http://127.0.0.1:8000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    if (!response.ok) throw new Error('API error');
    const data = await response.json();
    // data.label: 'REAL' or 'FAKE', data.confidence: float
    const prediction = data.label === 'REAL' ? 0 : 1;
    const confidence = data.confidence;
    lastPrediction = { prediction, confidence };
    return lastPrediction;
  } catch (e) {
    lastPrediction = { prediction: undefined, confidence: 0 };
    return lastPrediction;
  }
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === 'getPrediction') {
    sendResponse(lastPrediction);
  } else if (msg.action === 'submitFeedback') {
    // Optionally send feedback to a server
    console.log('User feedback:', msg.text);
  }
});

// Content script sends article text
chrome.runtime.onMessage.addListener((msg, sender) => {
  if (msg.action === 'analyzeArticle') {
    predict(msg.text).then(({ prediction, confidence }) => {
      chrome.action.setBadgeText({ text: prediction === 0 ? 'R' : (prediction === 1 ? 'F' : '?'), tabId: sender.tab.id });
      chrome.action.setBadgeBackgroundColor({ color: prediction === 0 ? '#2874f0' : (prediction === 1 ? '#e53935' : '#888'), tabId: sender.tab.id });
      chrome.runtime.sendMessage({ action: 'predictionReady', prediction, confidence });
    });
  }
});

chrome.runtime.onInstalled.addListener(() => {
  chrome.action.setBadgeText({ text: '' });
});
