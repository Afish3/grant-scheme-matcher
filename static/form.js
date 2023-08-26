const form = document.getElementById('question-form');
const questionContainer = getElementById("question");

    function getNextQuestion() {
        $.ajax({
            type: 'GET',
            url: '/form/question',
            success: function(data) {
                if (data.question !== null) {
                    questionContainer.html(data.question);
                    // Update form fields with new HTML
                    form.innerHTML = data.form;
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

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        // Serialize form data
        const formData = $(this).serializeArray();
        const answers = {};
        for (let i = 0; i < formData.length; i++) {
            const field = formData[i];
            answers[field.name] = field.value;
        }

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