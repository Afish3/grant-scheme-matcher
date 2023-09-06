const form = document.getElementById('question-form');
const question = document.getElementById('replace_with_current_question');
const submitButton = document.getElementById('submit-button');
const formToken = document.getElementById('form-token');
const questionContainer = $("#question-container");
    function getNextQuestion() {
        $.ajax({
            type: 'GET',
            url: '/form/question',
            success: function(data) {
                if (data.question !== null) {
                    questionContainer.html(data.question);
                    // Update form fields with new HTML
                    question.innerHTML = data.form;
                    console.log(data.form)
                } else {
                    questionContainer.text("Questionnaire completed!");
                    $("#submit-button").prop("disabled", true);
                }
            },
            error: function() {
                console.error("Error fetching question.");
            }
        });
    }

    submitButton.addEventListener('click', function(event) {
        event.preventDefault();
        // Serialize form data
        const inputs = document.querySelector('input[type="checkbox"]');
        console.log(inputs);
        const formData = $(form).serializeArray();
        const answers = {};
        for (let i = 0; i < formData.length; i++) {
            const field = formData[i];
            answers[field.name] = field.value;
        }
        console.log(answers)
    
        $.ajax({
            type: 'POST',
            url: '/form/question',
            contentType: 'application/json',
            data: JSON.stringify(answers),
            success: function() {
                getNextQuestion();
            },
            error: function() {
                console.error("Error posting answer.");
            }
        });
    });

    // Load initial question
    getNextQuestion();
    