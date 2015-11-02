jQuery(function(){
  $.confirm.options = {
      title: "Sicher?",
      text: "Sind Sie sich sicher?",
      confirmButton: "OK",
      cancelButton: "Abbrechen",
      post: false,
      confirmButtonClass: "btn-primary",
      cancelButtonClass: "btn-default",
      dialogClass: "modal-dialog",
      cancel: function(button) {}
  }

  $.rails.csrfToken = function() {
    return $.cookie('csrftoken');
  }

  $.rails.csrfParam = function() {
    return 'csrfmiddlewaretoken';
  }

  $.rails.CSRFProtection = function(xhr) {
    var token = $.rails.csrfToken();
    if (token) {
      xhr.setRequestHeader('X-CSRFToken', token);
    }
  }

  $.rails.showConfirmDialog = function($element) {
    var message;

    if ($element.data('confirm-custom')) {
      message = $element.data('confirm-custom');
    } else {
      var subject = " ";
      if ($element.data('confirm-subject')) {
        subject = $element.data('confirm-subject') + ' ';
      }
      message = "Soll der Eintrag"+subject+"wirklich gelöscht werden?";
    }

    var confirmButton = $element.data('confirm-ok') || 'Löschen';

    $.confirm({
      text: message,
      title: "Sicher?",
      confirm: function(button) {
        $.rails.confirmed($element)
      },
      confirmButton: confirmButton,
      confirmButtonClass: "btn-danger"
    });
  };

  $.rails.allowAction = function($element) {
    if (!$element.attr('data-confirm')) {
      return true;
    }
    $.rails.showConfirmDialog($element);
    return false;
  }

  $.rails.confirmed = function($element) {
    $element.removeAttr('data-confirm');
    $element.trigger('click.rails');
    if (!$element.data('method') && !$element.data('remote')) {
      window.location = $element.context.href;
    }
  }
});
