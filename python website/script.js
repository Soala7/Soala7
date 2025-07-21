document.addEventListener('DOMContentLoaded', function() {
    const quizContainer = document.getElementById('quiz');
    const resultsContainer = document.getElementById('results');
    const submitButton = document.getElementById('submit');
    
    // Quiz questions with answers and difficulty levels
    const questions = [
        {
            question: "What is the output of: print(type(5))?",
            options: ["<class 'int'>", "<class 'str'>", "<class 'float'>", "Error"],
            answer: 0,
            difficulty: "beginner"
        },
        {
            question: "How do you create an empty list in Python?",
            options: ["list()", "[]", "Both A and B", "None of the above"],
            answer: 2,
            difficulty: "beginner"
        },
        {
            question: "What does the 'range(3, 8, 2)' function return?",
            options: ["[3, 5, 7]", "[3, 4, 5, 6, 7]", "[3, 8, 2]", "Error"],
            answer: 0,
            difficulty: "intermediate"
        },
        {
            question: "What is the purpose of __init__ in a Python class?",
            options: [
                "It initializes the class namespace",
                "It's called when an object is created",
                "It's a constructor method",
                "All of the above"
            ],
            answer: 3,
            difficulty: "intermediate"
        },
        {
            question: "What will 'print([x**2 for x in range(5)])' output?",
            options: ["[0, 1, 4, 9, 16]", "[1, 4, 9, 16, 25]", "[0, 1, 4, 9]", "Error"],
            answer: 0,
            difficulty: "intermediate"
        },
        {
            question: "What is the output of: print(*(x for x in range(3)))?",
            options: ["0 1 2", "(0, 1, 2)", "[0, 1, 2]", "Error"],
            answer: 0,
            difficulty: "advanced"
        },
        {
            question: "What does the @property decorator do?",
            options: [
                "Makes a method callable like an attribute",
                "Converts a method to a class method",
                "Marks a method as static",
                "None of the above"
            ],
            answer: 0,
            difficulty: "advanced"
        },
        {
            question: "What is method resolution order (MRO) in Python?",
            options: [
                "The order in which methods are executed",
                "The order Python searches for attributes in inheritance",
                "The order of method parameters",
                "None of the above"
            ],
            answer: 1,
            difficulty: "advanced"
        },
        {
            question: "What is the purpose of __slots__ in a Python class?",
            options: [
                "To limit attribute creation",
                "To improve memory usage",
                "To make attributes read-only",
                "Both A and B"
            ],
            answer: 3,
            difficulty: "advanced"
        },
        {
            question: "What does the 'yield from' statement do?",
            options: [
                "Delegates to a subgenerator",
                "Returns from a generator",
                "Yields all values from an iterable",
                "Both A and C"
            ],
            answer: 3,
            difficulty: "advanced"
        }
    ];

    // Display quiz questions
    function displayQuiz() {
        questions.forEach((question, index) => {
            const questionElement = document.createElement('div');
            questionElement.classList.add('question');
            
            const questionText = document.createElement('h3');
            questionText.textContent = `${index + 1}. ${question.question}`;
            questionElement.appendChild(questionText);
            
            const optionsElement = document.createElement('div');
            optionsElement.classList.add('options');
            
            question.options.forEach((option, optionIndex) => {
                const optionElement = document.createElement('div');
                optionElement.classList.add('option');
                
                const input = document.createElement('input');
                input.type = 'radio';
                input.name = `question${index}`;
                input.value = optionIndex;
                input.id = `q${index}o${optionIndex}`;
                
                const label = document.createElement('label');
                label.htmlFor = `q${index}o${optionIndex}`;
                label.textContent = option;
                
                optionElement.appendChild(input);
                optionElement.appendChild(label);
                optionsElement.appendChild(optionElement);
            });
            
            questionElement.appendChild(optionsElement);
            quizContainer.appendChild(questionElement);
        });
    }

    // Calculate results and determine level
    function calculateResults() {
        let score = 0;
        let beginnerCorrect = 0;
        let intermediateCorrect = 0;
        let advancedCorrect = 0;
        
        questions.forEach((question, index) => {
            const selectedOption = document.querySelector(`input[name="question${index}"]:checked`);
            
            if (selectedOption) {
                if (parseInt(selectedOption.value) === question.answer) {
                    score++;
                    
                    // Track correct answers by difficulty
                    if (question.difficulty === "beginner") {
                        beginnerCorrect++;
                    } else if (question.difficulty === "intermediate") {
                        intermediateCorrect++;
                    } else {
                        advancedCorrect++;
                    }
                }
            }
        });
        
        // Determine user level based on performance
        let level;
        if (advancedCorrect >= 3) {
            level = "advanced";
        } else if (intermediateCorrect >= 3 || (intermediateCorrect >= 2 && beginnerCorrect >= 4)) {
            level = "intermediate";
        } else {
            level = "beginner";
        }
        
        // Display results and redirect
        resultsContainer.style.display = 'block';
        resultsContainer.innerHTML = `
            <h2>Your Results</h2>
            <p>You scored ${score} out of ${questions.length}</p>
            <p>Your Python level: <strong>${level.charAt(0).toUpperCase() + level.slice(1)}</strong></p>
            <p>Redirecting you to the appropriate resources...</p>
        `;
        
        // Redirect after 3 seconds
        setTimeout(() => {
            window.location.href = `${level}.html`;
        }, 3000);
    }

    // Event listeners
    submitButton.addEventListener('click', calculateResults);
    
    // Initialize quiz
    displayQuiz();
});