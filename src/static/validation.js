/* This JavaScript Code is used for form validation in quizzes
If a required field is not filled out, it will prevent form submission
and display an error message */

(function() {
  'use strict';
  window.addEventListener('load', function() {
    // Fetch all the forms which need validation as specified in the class name
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();
