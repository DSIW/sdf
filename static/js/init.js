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
  $('textarea').trigger('autoresize');
  $('.tooltipped').tooltip({position: 'top', delay: 15});
  $('.nav-fixed .tooltipped').tooltip({position: 'bottom', delay: 15});
  $('input[type=checkbox]').addClass('filled-in');
  $('input[type=checkbox] + label').on('click', function(event) {
    $(this).siblings('input').click();
  });

  $('.js-alert-hide').on('click', function(event) {
    $(this).parents('.alert').fadeOut();
  });

  $('#arrow-scroller').on('click', function(event) {
    $.scrollTo('#books', 500);
  });

  $("nav[role=navigation] ul.navigation-bar li").each(function(index, element) {
    $element = $(element);
    href = $element.find('a').first().attr('href');
    href = URI(href || "").path();
    currentPath = document.location.pathname;
    if (currentPath.indexOf(href) >= 0) {
      $element.addClass('active');
    }
  });
});
