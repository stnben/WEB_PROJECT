const user_id = "user1"; // Replace with a unique user ID

$("#set-preferences").on("submit", function (event) {
    event.preventDefault();

    const userName = $("#user_name").val();
    const interviewDuration = $("#interview_duration").val();
    const position = $("#position").val();
    const num_questions = $("#num_questions").val();
    const difficulty = $("#difficulty").val();
    const category = $("#category").val();

    $.ajax({
        url: '/api/set_preferences',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            user_id,
            userName,
            interviewDuration,
            position,
            num_questions,
            difficulty,
            category
        }),
        success: function () {
            $("#preferences-form").hide();
            $("#interview").show();
        }
    });
});

$("#send-message").on("submit", function (event) {
    event.preventDefault();

    const input = $("#user-input").val();
    $("#user-input").val("");

    $("#messages").append(`<p>User: ${input}</p>`);

    const data = {
        user_id,
        input
    };

    console.log("Sending data:", data);

    $.ajax({
        url: '/api/handle_message',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (data) {
            if (data.action === "analyze_performance") {
                $("#analyze-performance").show();
            } else {
                const ai_response = data.response;
                $("#messages").append(`<p>AI: ${ai_response}</p>`);
            }
        }
    });
});

