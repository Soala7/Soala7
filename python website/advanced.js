document.addEventListener('DOMContentLoaded', function() {
  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        window.scrollTo({
          top: targetElement.offsetTop - 20,
          behavior: 'smooth'
        });
        
        // Update URL without page jump
        history.pushState(null, null, targetId);
      }
    });
  });

  // Add copy button to code blocks
  document.querySelectorAll('.code-block').forEach(codeBlock => {
    const copyButton = document.createElement('button');
    copyButton.innerHTML = '<i class="fas fa-copy"></i>';
    copyButton.className = 'copy-button';
    copyButton.title = 'Copy to clipboard';
    
    codeBlock.style.position = 'relative';
    copyButton.style.position = 'absolute';
    copyButton.style.top = '5px';
    copyButton.style.right = '5px';
    copyButton.style.background = 'transparent';
    copyButton.style.border = 'none';
    copyButton.style.color = '#abb2bf';
    copyButton.style.cursor = 'pointer';
    copyButton.style.padding = '5px';
    copyButton.style.borderRadius = '3px';
    
    copyButton.addEventListener('mouseenter', () => {
      copyButton.style.color = 'white';
      copyButton.style.background = 'rgba(255, 255, 255, 0.2)';
    });
    
    copyButton.addEventListener('mouseleave', () => {
      copyButton.style.color = '#abb2bf';
      copyButton.style.background = 'transparent';
    });
    
    copyButton.addEventListener('click', () => {
      const code = codeBlock.querySelector('code').textContent;
      navigator.clipboard.writeText(code).then(() => {
        copyButton.innerHTML = '<i class="fas fa-check"></i>';
        copyButton.style.color = 'var(--success-color)';
        setTimeout(() => {
          copyButton.innerHTML = '<i class="fas fa-copy"></i>';
          copyButton.style.color = '#abb2bf';
        }, 2000);
      });
    });
    
    codeBlock.appendChild(copyButton);
  });

  // Collapsible sections
  document.querySelectorAll('h2').forEach(header => {
    header.style.cursor = 'pointer';
    header.addEventListener('click', () => {
      const section = header.parentElement;
      const content = Array.from(section.children).filter(
        child => child !== header
      );
      
      content.forEach(el => {
        if (el.style.display === 'none') {
          el.style.display = '';
          section.style.paddingBottom = '1.5rem';
        } else {
          el.style.display = 'none';
          section.style.paddingBottom = '0.5rem';
        }
      });
    });
  });

  // Syntax highlighting (would be more robust with a library like Prism.js)
  document.querySelectorAll('.code-block code').forEach(codeElement => {
    const code = codeElement.textContent;
    // Simple keyword highlighting
    const keywords = [
      'def', 'class', 'return', 'yield', 'import', 'from', 'as',
      'if', 'else', 'elif', 'for', 'while', 'try', 'except',
      'finally', 'with', 'async', 'await', 'lambda'
    ];
    
    let highlightedCode = code;
    
    keywords.forEach(keyword => {
      const regex = new RegExp(`\\b${keyword}\\b`, 'g');
      highlightedCode = highlightedCode.replace(
        regex,
        `<span class="keyword">${keyword}</span>`
      );
    });
    
    // Highlight strings
    highlightedCode = highlightedCode.replace(
      /(['"])(.*?)\1/g,
      '<span class="string">$1$2$1</span>'
    );
    
    // Highlight numbers
    highlightedCode = highlightedCode.replace(
      /\b(\d+)\b/g,
      '<span class="number">$1</span>'
    );
    
    // Highlight comments
    highlightedCode = highlightedCode.replace(
      /(#.*$)/gm,
      '<span class="comment">$1</span>'
    );
    
    codeElement.innerHTML = highlightedCode;
  });

  // Add a back-to-top button
  const backToTopButton = document.createElement('button');
  backToTopButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
  backToTopButton.id = 'back-to-top';
  backToTopButton.title = 'Back to top';
  backToTopButton.style.display = 'none';
  backToTopButton.style.position = 'fixed';
  backToTopButton.style.bottom = '20px';
  backToTopButton.style.right = '20px';
  backToTopButton.style.zIndex = '99';
  backToTopButton.style.border = 'none';
  backToTopButton.style.outline = 'none';
  backToTopButton.style.backgroundColor = 'var(--primary-color)';
  backToTopButton.style.color = 'white';
  backToTopButton.style.cursor = 'pointer';
  backToTopButton.style.padding = '15px';
  backToTopButton.style.borderRadius = '50%';
  backToTopButton.style.fontSize = '18px';
  backToTopButton.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
  
  backToTopButton.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
  
  document.body.appendChild(backToTopButton);
  
  window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
      backToTopButton.style.display = 'block';
    } else {
      backToTopButton.style.display = 'none';
    }
  });

  // Add print button
  const printButton = document.createElement('button');
  printButton.innerHTML = '<i class="fas fa-print"></i> Print Guide';
  printButton.id = 'print-button';
  printButton.style.position = 'fixed';
  printButton.style.bottom = '20px';
  printButton.style.left = '20px';
  printButton.style.zIndex = '99';
  printButton.style.padding = '10px 15px';
  printButton.style.backgroundColor = 'var(--dark-color)';
  printButton.style.color = 'white';
  printButton.style.border = 'none';
  printButton.style.borderRadius = '5px';
  printButton.style.cursor = 'pointer';
  printButton.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
  
  printButton.addEventListener('click', () => {
    window.print();
  });
  
  document.body.appendChild(printButton);
});