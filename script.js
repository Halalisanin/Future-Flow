// Contact form validation
document.querySelector('.contact-form')?.addEventListener('submit', function (e) {
  const name = this.querySelector('input[type="text"]').value.trim();
  const email = this.querySelector('input[type="email"]').value.trim();
  const message = this.querySelector('textarea').value.trim();
  if (!name || !email || !message) {
    alert('Please fill in all fields before sending.');
    e.preventDefault();
  }
});

// Newsletter → Audienceful
document.getElementById('newsletter-form')?.addEventListener('submit', async function (e) {
  e.preventDefault();
  const email = document.getElementById('newsletter-email').value.trim();
  if (!email) return alert('Enter your email to subscribe.');

  const response = await fetch('https://api.audienceful.com/forms/submit', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer lL8qI3TM.hRQT7eGgcTJG9wYxdd9SdT47bWJCUvBn'
    },
    body: JSON.stringify({
      form: 'newsletter',
      fields: { email }
    })
  });

  if (response.ok) {
    alert('Thanks for subscribing!');
    this.reset();
  } else {
    alert('Something went wrong. Please try again later.');
  }
});

// Poll vote tracking
document.querySelectorAll('.poll button').forEach(button => {
  button.addEventListener('click', () => {
    localStorage.setItem('futureflow_vote', button.textContent);
    alert(`Thanks for voting: ${button.textContent}`);
  });
});

// Tool submission confirmation
document.querySelector('.submit-tool')?.addEventListener('submit', function (e) {
  const name = this.querySelector('input[type="text"]').value.trim();
  const link = this.querySelector('input[type="url"]').value.trim();
  if (!name || !link) {
    alert('Please enter both tool name and link.');
    e.preventDefault();
  } else {
    alert('Tool submitted! Thanks for contributing.');
  }
});

// Emoji reactions
function react(emoji) {
  alert(`You reacted with ${emoji}!`);
}

// Gemini → Google AI Studio
async function askGemini(promptText) {
  const response = await fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyADxJ0ZeJJpmfU_ieiKhFcOvIGxICQHraM', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      contents: [{ parts: [{ text: promptText }] }]
    })
  });
  const data = await response.json();
  const reply = data?.candidates?.[0]?.content?.parts?.[0]?.text;
  console.log('Gemini says:', reply);
  return reply;
}

// OpenRouter → AI Chat
async function askOpenRouter(promptText) {
  const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer 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'
    },
    body: JSON.stringify({
      model: 'mistral/mistral-7b-instruct',
      messages: [{ role: 'user', content: promptText }]
    })
  });
  const data = await response.json();
  const reply = data?.choices?.[0]?.message?.content;
  console.log('OpenRouter says:', reply);
  return reply;
}

// AI Playground interaction
async function runGemini() {
  const prompt = document.getElementById('user-prompt').value.trim();
  if (!prompt) return alert('Type something first!');
  const reply = await askGemini(prompt);
  document.getElementById('ai-response').innerText = reply || 'No response.';
}

async function runOpenRouter() {
  const prompt = document.getElementById('user-prompt').value.trim();
  if (!prompt) return alert('Type something first!');
  const reply = await askOpenRouter(prompt);
  document.getElementById('ai-response').innerText = reply || 'No response.';
}

