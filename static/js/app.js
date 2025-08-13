// clbientside form validation ( bootstrap style)+small helpers
(() => {
    'use strict';
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
      form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  })();
  
  // fallback filter if JS filter bugs out
  document.querySelectorAll('[data-add-class]').forEach(el => {
    el.classList.add(el.getAttribute('data-add-class'));
  });
  