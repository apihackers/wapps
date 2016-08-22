$(function() {
	var MESSAGES = {
		en: {
			words: '<strong>{count}</strong> word(s)',
			chars: '<strong>{count}</strong> char(s)',
			charsMax: '<strong>{count}/{max}</strong> char(s)'
		},
		fr: {
			words: '<strong>{count}</strong> mot(s)',
			chars: '<strong>{count}</strong> caractère(s)',
			charsMax: '<strong>{count}/{max}</strong> caractère(s)',
		}
	};

	var LANG = $('html').attr('lang').split('-')[0];
	LANG = 'fr';

	function countWords(text) {
		return text.trim().split(/\s+/).length
	}

	function countChars(text) {
		return text.length - 1;
	}

	function extractText(el) {
		text = "";
		var length = el.childNodes.length;
		for (var i = 0; i < length; i++) {
			var node = el.childNodes[i];
			if (node.nodeType != 8) {  // Skip comments
				text += node.nodeType != 1 ? node.nodeValue : extractText(node);
			}
		}
		return text;
	}

	function getHelp($el) {
		var $help = $el.closest('.object').find('.object-help');
		if (!$help) {
			$help = $('<div style="opacity:1;" class="object-help help"></div>');
			$help.appendTo($el.closest('.object'));
		}
		var $container = $('<div class="text-counter"></div>').appendTo($help);
		return [$help, $container];
	}

	function setCounter($container, text, maxlength) {
		var words = countWords(text);
		var chars = countChars(text);
		var wordsTxt = MESSAGES[LANG].words.replace('{count}', words);
		var charsTpl = maxlength ?  MESSAGES[LANG].charsMax : MESSAGES[LANG].chars;
		var charsTxt = charsTpl.replace('{count}', chars).replace('{max}', maxlength);
		$container.html([
			'<div class="word-counter">', wordsTxt, '</div>',
			'<div class="chars-counter">', charsTxt, '</div>',
		].join(''));
	}

	$('.richtext').each(function() {
		var $richtext = $(this);
		var $textarea = $richtext.next('textarea');
		var [$help, $container] = getHelp($richtext);
		setCounter($container, extractText($richtext[0]), $textarea.attr('maxlength'));
		$richtext.on('hallomodified', function() {
			setCounter($container, extractText($richtext[0]), $textarea.attr('maxlength'));
		})
	});
	$('.field.char_field:not(.hallo_rich_text_area) input').each(function() {
		var $input = $(this);
		var [$help, $container] = getHelp($input);
		setCounter($container, $input.val(), $input.attr('maxlength'));
		$input.on('change', function() {
			setCounter($container, $input.val(), $input.attr('maxlength'));
		})
	});

	$('.field.char_field:not(.hallo_rich_text_area) textarea').each(function() {
		var $textarea = $(this);
		var [$help, $container] = getHelp($textarea);
		setCounter($container, $textarea.val(), $textarea.attr('maxlength'));
		$textarea.on('change', function() {
			setCounter($container, $textarea.val(), $textarea.attr('maxlength'));
		})
	});
});
