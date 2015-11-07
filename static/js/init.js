jQuery(function(){
  $('.button-collapse').sideNav();
  $('.parallax').parallax();
  $('select').material_select();
  $('.datepicker').pickadate({
    format: 'dd.mm.yyyy',
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 15 // Creates a dropdown of 15 years to control year
  });
  $('textarea').addClass('materialize-textarea');
  $('input[type=checkbox]').addClass('filled-in');
  $('input[type=checkbox] + label').on('click', function(event) {
    $(this).siblings('input').click();
  });

  $('.js-alert-hide').on('click', function(event) {
    $(this).parents('.alert').fadeOut();
  });
});
