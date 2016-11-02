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
		return text.length;
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
        var $help, $container;
        var $object = $el.closest('.object');
        if ($object.hasClass('char_field')) {
            // This is a single field panel
            $help = $object.find('.object-help');
            if (!$help.length) {
                $help = $('<div style="opacity:1;" class="object-help help"></div>');
                $help.appendTo($object);
            }
            $container = $('<div class="text-counter"></div>').appendTo($help)
        } else {
            var $fieldContent = $el.closest('.field-content');
            $help = $fieldContent.find('.help');
            if (!$help.length) {
                $help = $('<p class="help"></p>');
                $help.appendTo($fieldContent);
            }
            $container = $('<div class="text-counter one-line"></div>').appendTo($help)
        }
		return [$help, $container];
	}

	function setCounter($container, text, maxlength) {
		var words = countWords(text);
		var chars = countChars(text);
		var wordsTxt = MESSAGES[LANG].words.replace('{count}', words);
		var charsTpl = maxlength ?  MESSAGES[LANG].charsMax : MESSAGES[LANG].chars;
		var charsTxt = charsTpl.replace('{count}', chars).replace('{max}', maxlength);
		if (chars <= 0) {
			$container.empty();
		} else if ($container.hasClass('one-line')) {
			$container.html([
				'<i>',
				'<span class="word-counter">', wordsTxt, '</span>',
				' / ',
				'<span class="chars-counter">', charsTxt, '</span>',
				'</i>'
			].join(''));
		} else {
			$container.html([
				'<div class="word-counter">', wordsTxt, '</div>',
				'<div class="chars-counter">', charsTxt, '</div>',
			].join(''));
		}
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
	$('.field.char_field:not(.widget-hallo_rich_text_area):not(.hallo_rich_text_area):not(.no-counter) input').each(function() {
		var $input = $(this);
		var [$help, $container] = getHelp($input);
		setCounter($container, $input.val(), $input.attr('maxlength'));
		$input.on('change keyup paste', function() {
			setCounter($container, $input.val(), $input.attr('maxlength'));
		})
	});

	$('.field.char_field:not(.widget-hallo_rich_text_area):not(.hallo_rich_text_area):not(.no-counter) textarea').each(function() {
		var $textarea = $(this);
		var [$help, $container] = getHelp($textarea);
		setCounter($container, $textarea.val(), $textarea.attr('maxlength'));
		$textarea.on('change keyup paste', function() {
			setCounter($container, $textarea.val(), $textarea.attr('maxlength'));
		})
	});
});
