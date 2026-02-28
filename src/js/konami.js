// Konami Code Easter Egg
// ↑ ↑ ↓ ↓ ← → ← → B A
(function() {
  const konamiCode = [
    'ArrowUp', 'ArrowUp',
    'ArrowDown', 'ArrowDown',
    'ArrowLeft', 'ArrowRight',
    'ArrowLeft', 'ArrowRight',
    'b', 'a'
  ];
  
  let konamiIndex = 0;
  let konamiTimer = null;
  
  // Create toast element
  const toast = document.createElement('div');
  toast.className = 'konami-toast';
  toast.innerHTML = `
    <div class="konami-toast-content">
      <span class="konami-toast-icon">🎮</span>
      <div class="konami-toast-text">
        <strong>Konami Code Activated!</strong>
        <span>You've unlocked secret mode. Check the console.</span>
      </div>
    </div>
  `;
  document.body.appendChild(toast);
  
  // Secret messages to log
  const secrets = [
    '🎮 Konami Code Activated!',
    '',
    'Hey there, curious one!',
    '',
    'Fun facts about this site:',
    '• Built with Eleventy static site generator',
    '• Hosted on GitHub Pages',
    '• Design inspired by Swiss minimalism',
    '• Hidden projects accessible via direct URLs',
    '',
    '',
    'Want to work together?',
    'Email: hello@menilvukovic.com',
    '',
    '— Menil'
  ];
  
  function showKonamiToast() {
    toast.classList.add('show');
    
    // Log secrets to console
    console.log(secrets.join('\n'));
    
    // Hide after 5 seconds
    setTimeout(() => {
      toast.classList.remove('show');
    }, 5000);
    
    // Reset
    konamiIndex = 0;
  }
  
  document.addEventListener('keydown', (e) => {
    // Clear timer on any keypress
    if (konamiTimer) {
      clearTimeout(konamiTimer);
    }
    
    // Check if key matches expected key in sequence
    const expectedKey = konamiCode[konamiIndex];
    
    if (e.key.toLowerCase() === expectedKey.toLowerCase()) {
      konamiIndex++;
      
      // Check if code is complete
      if (konamiIndex === konamiCode.length) {
        showKonamiToast();
      } else {
        // Set timer to reset if no key pressed for 2 seconds
        konamiTimer = setTimeout(() => {
          konamiIndex = 0;
        }, 2000);
      }
    } else {
      // Wrong key, reset
      konamiIndex = 0;
    }
  });
})();
