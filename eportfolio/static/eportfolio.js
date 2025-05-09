document.addEventListener("DOMContentLoaded", function() {
    var forms = document.querySelectorAll("form"); 

    forms.forEach(function(form) {
        form.addEventListener("submit", function(event) {
            event.preventDefault(); 

            let submitButton = this.querySelector("[type=submit]");
            submitButton.disabled = true;

            setTimeout(function() {
                submitButton.disabled = false;
            }, 10000);

            this.submit();
        });
    });

    var cancelButtons = document.querySelectorAll(".btn-cancel");
    cancelButtons.forEach(function(cancelButton) {
        cancelButton.addEventListener("click", function(event) {
            event.preventDefault(); // Prevent default action
            history.back();
        });
    });
});