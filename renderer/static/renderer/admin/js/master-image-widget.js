(function ($) {

	function onInputImageChanged (input) {
		var $i = $(input);
		var url = $i.data('get-rendition-url') + $i.val() + '/100/0/';
		var masterUrl = $i.data('get-master-url');
		var $container = $i.parent().find('.master-image-preview');

		$container.addClass('loading');
		$container.empty();

		$.getJSON(url, function (data) {
			$container.append('<a target="_blank" href="' + masterUrl + '"><img src="' + data.url + '"/></a>');
			$container.removeClass('hidden');
			$container.removeClass('loading');
		});
	}

	// monkey patch related popup that does not trigger a value change
	var old_dismissRelatedLookupPopup = window.dismissRelatedLookupPopup;
	window.dismissRelatedLookupPopup = function (win, chosenId) {
		old_dismissRelatedLookupPopup(win, chosenId);
		$('#' + window.windowname_to_id(win.name)).change();
	};
	$(document).ready(function () {
		$('.vForeignKeyRawIdAdminField')
			.each(function () {
				// setup
				var $i = $(this);
				var $p = $i.parent();

				$p.append('<div class="master-image-preview hidden"/>');

				if ($i.val().length > 0) onInputImageChanged(this);
			})
			.on('change propertychange input', function () {
				onInputImageChanged(this);
			})
		;
	});
})(django.jQuery);
