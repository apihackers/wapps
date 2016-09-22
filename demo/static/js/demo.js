function parentForm(el) {
    while(el.parentNode) {
        el = el.parentNode;
        if (el.tagName.toLowerCase() === 'form') return el;
    }
}

function changeLang(ev, el, lang) {
    ev.preventDefault();
    var form = parentForm(el);
    form.querySelector('[name=next]').value = window.location.href;
    form.querySelector('[name=language]').value = lang;
    form.submit();
    return false;
}
