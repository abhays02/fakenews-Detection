// Extracts article text and sends to background for analysis
function getArticleText() {
  // Simple heuristic: get main text from <article> or <p> tags
  let article = document.querySelector('article');
  if (article) return article.innerText;
  let ps = Array.from(document.querySelectorAll('p'));
  let text = ps.map(p => p.innerText).join(' ');
  return text.length > 100 ? text : '';
}

const text = getArticleText();
if (text) {
  chrome.runtime.sendMessage({ action: 'analyzeArticle', text });
}
