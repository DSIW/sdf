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

  $('#arrow-scroller').on('click', function(event) { $.scrollTo('#books', 500); });
  $('#arrow-scroller1').on('click', function(event) { $.scrollTo('#books', 500); });
  $('#arrow-scroller2').on('click', function(event) { $.scrollTo('#books', 500); });

  $("nav[role=navigation] ul.navigation-bar li").each(function(index, element) {
    $element = $(element);
    href = $element.find('a').first().attr('href');
    href = URI(href || "").path();
    currentPath = document.location.pathname;
    if (currentPath.indexOf(href) >= 0) {
      $element.addClass('active');
    }
  });

  $('.card-book').each(function ()
  {
    var targetParent = $(this).find(".card-content > p.book-title");
    var target = targetParent.find("span");
    var target2 = $(this).find(".card-reveal > span.card-title");

    while( target.outerHeight() > targetParent.outerHeight() )
    {
        var smalerFontSize = parseFloat( target.css("font-size") )-1;
        if(smalerFontSize < 10)
        {
          targetParent.css("text-overflow", "ellipsis");
          target2.css("text-overflow", "ellipsis");
          break;
        }

        targetParent.css("font-size", smalerFontSize+"px");
        target2.css("font-size", smalerFontSize+"px");
    }
  });
});

