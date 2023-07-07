(function($) {
	"use strict";
  
	// Form
	var contactForm = function() {
	  if ($('#contactForm').length > 0 ) {
		$("#contactForm").validate({
		  rules: {
			name: "required",
			subject: "required",
			email: {
			  required: true,
			  email: true
			},
			message: {
			  required: true,
			  minlength: 5
			}
		  },
		  messages: {
			name: "Please enter your name",
			subject: "Please enter your subject",
			email: "Please enter a valid email address",
			message: "Please enter a message"
		  },
		  /* submit via ajax */
		  submitHandler: function(form) {
			var $submit = $('.submitting');
			var waitText = 'Submitting...';
			var url = $(form).data('url'); // Get the URL from data attribute
  
			$.ajax({
			  type: "POST",
			  url: url,
			  data: $(form).serialize(),
			  beforeSend: function() {
				$submit.css('display', 'block').text(waitText);
			  },
			  success: function(msg) {
				if (msg == 'OK') {
				  $('#form-message-warning').hide();
				  setTimeout(function() {
					$('#contactForm').fadeIn();
				  }, 1000);
				  setTimeout(function() {
					$('#form-message-success').fadeIn();
				  }, 1400);
  
				  setTimeout(function() {
					$('#form-message-success').fadeOut();
				  }, 8000);
  
				  setTimeout(function() {
					$submit.css('display', 'none').text(waitText);
				  }, 1400);
  
				  setTimeout(function() {
					$('#contactForm')[0].reset(); // Reset the form
				  }, 1400);
  
				} else {
				  $('#form-message-warning').html(msg);
				  $('#form-message-warning').fadeIn();
				  $submit.css('display', 'none');
				}
			  },
			  error: function() {
				$('#form-message-warning').html("Something went wrong. Please try again.");
				$('#form-message-warning').fadeIn();
				$submit.css('display', 'none');
			  }
			});
		  }
		});
	  }
	};
	
	contactForm();
  
  })(jQuery);
  