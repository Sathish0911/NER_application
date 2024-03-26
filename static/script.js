$(document).ready(function () {
    $("#submitBtn").click(function () {
        var inputText;
        var formData = new FormData();

        // Check if text input is provided
        if ($("#input_text").val().trim() !== "") {
            inputText = $("#input_text").val();
            formData.append('input_text', inputText);
        } else {
            // Check if a file is uploaded
            var file = $('#file_input').prop('files')[0];
            if (!file) {
                alert("Please enter text or upload a file.");
                return;
            }
            formData.append('file', file);
        }

        $.ajax({
            url: "/",
            type: "POST",
            processData: false,
            contentType: false,
            data: formData,
            success: function (response) {
                $("#output").html(response.output_text); // Set HTML content to the <div>
                $("#downloadLink").attr("href", response.download_link);
                $("#downloadBtn").prop("disabled", false);
            }
        });
    });

    $("#resetBtn").click(function () {
        $("#input_text").val("");
        $("#output").html(""); // Clear HTML content
        $("#downloadLink").attr("href", "#");
        $("#downloadBtn").prop("disabled", true);

        // Clear the selected file in the file input field
        $("#file_input").val("");
    });
});