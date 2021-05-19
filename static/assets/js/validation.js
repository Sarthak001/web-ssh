$( document ).ready(function() {

  (function () {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
      .forEach(function (form) {
        form.addEventListener('submit', function (event) {
          if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()      
          }
          form.classList.add('was-validated')
        }, false)
      })
  })()


$('.radio-check').click(function check(){

  if($('input[name="auth"]:checked').val() == "password"){
      $("#pass").removeClass("d-none");
      $("#key").addClass("d-none");
      $('#input-pass').prop('required',true);


  }
  else{
    $("#key").removeClass("d-none");
    $("#pass").addClass("d-none");
    $('#input-key').prop('required',true);


  }






})



});
