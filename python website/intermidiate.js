// Define quiz questions at the top level
const quizQuestions = [
  {
    question: "What keyword is used to define a function in Python?",
    options: ["func", "def", "function", "define"],
    answer: 1
  },
  {
    question: "Which of these is NOT a magic method in Python?",
    options: ["__init__", "__str__", "__call__", "__magic__"],
    answer: 3
  },
  {
    question: "How do you import a specific function from a module?",
    options: [
      "import function from module",
      "from module import function",
      "module.import(function)",
      "require module.function"
    ],
    answer: 1
  },
  {
    question: "What is the correct way to open a file for reading?",
    options: [
      "open('file.txt', 'read')",
      "open('file.txt', 'r')",
      "open('file.txt', 'readonly')",
      "open('file.txt')"
    ],
    answer: 1
  },
  {
    question: "Which exception is raised when dividing by zero?",
    options: [
      "ValueError",
      "ZeroDivisionError",
      "ArithmeticError",
      "DivisionError"
    ],
    answer: 1
  }
];

document.addEventListener('DOMContentLoaded', function() {
  // ... (keep all your existing DOMContentLoaded code) ...

  // Initialize the quiz button
  const quizButton = document.querySelector('.quiz-button');
  if (quizButton) {
    quizButton.addEventListener('click', startQuiz);
  }
});

// Quiz functions
function startQuiz() {
  const modal = document.getElementById('quiz-modal');
  const quizContainer = document.getElementById('quiz-container');
  
  // Clear previous quiz if any
  quizContainer.innerHTML = '';
  
  // Generate quiz questions
  quizQuestions.forEach((question, index) => {
    const questionElement = document.createElement('div');
    questionElement.className = 'quiz-question';
    questionElement.innerHTML = `
      <h3>${index + 1}. ${question.question}</h3>
      ${question.options.map((option, optionIndex) => `
        <div class="quiz-option">
          <input type="radio" id="q${index}-opt${optionIndex}" name="q${index}" value="${optionIndex}">
          <label for="q${index}-opt${optionIndex}">${option}</label>
        </div>
      `).join('')}
    `;
    quizContainer.appendChild(questionElement);
  });

  // Create submit button if it doesn't exist
  if (!document.getElementById('submit-quiz')) {
    const submitButton = document.createElement('button');
    submitButton.id = 'submit-quiz';
    submitButton.textContent = 'Submit Quiz';
    submitButton.addEventListener('click', submitQuiz);
    quizContainer.appendChild(submitButton);
  }

  // Create results container if it doesn't exist
  if (!document.getElementById('quiz-results')) {
    const resultsContainer = document.createElement('div');
    resultsContainer.id = 'quiz-results';
    quizContainer.appendChild(resultsContainer);
  } else {
    document.getElementById('quiz-results').innerHTML = '';
  }

  modal.style.display = 'block';
  document.body.style.overflow = 'hidden';
}

function submitQuiz() {
  const resultsContainer = document.getElementById('quiz-results');
  let score = 0;
  const totalQuestions = quizQuestions.length;
  
  // Check each question
  quizQuestions.forEach((question, index) => {
    const selectedOption = document.querySelector(`input[name="q${index}"]:checked`);
    if (selectedOption && parseInt(selectedOption.value) === question.answer) {
      score++;
    }
  });
  
  const percentage = Math.round((score / totalQuestions) * 100);
  let message = '';
  
  if (percentage >= 80) {
    message = `<p class="quiz-result excellent">Excellent! You scored ${score}/${totalQuestions} (${percentage}%)</p>`;
  } else if (percentage >= 50) {
    message = `<p class="quiz-result good">Good effort! You scored ${score}/${totalQuestions} (${percentage}%)</p>`;
  } else {
    message = `<p class="quiz-result poor">Keep practicing! You scored ${score}/${totalQuestions} (${percentage}%)</p>`;
  }
  
  resultsContainer.innerHTML = message;
  
  // Scroll to results
  resultsContainer.scrollIntoView({ behavior: 'smooth' });
}

function closeModal() {
  document.getElementById('quiz-modal').style.display = 'none';
  document.body.style.overflow = '';
}

// ... (keep all your other existing functions) ...