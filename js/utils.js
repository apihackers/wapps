/**
 * Get nearest parent element matching selector
 */
export function closest(el, selector) {
    var matchesSelector = el.matches || el.webkitMatchesSelector || el.mozMatchesSelector || el.msMatchesSelector;
    while (el) {
        if (matchesSelector.call(el, selector)) break;
        el = el.parentElement;
    }
    return el;
}

export function viewTop() {
    return document.body.scrollTop || document.documentElement.scrollTop; // Firefox + Chrome
}

export function inViewport(el) {
    const view_top = viewTop(); // Firefox + Chrome
    const view_bottom = view_top + window.innerHeight;
    const el_top = el.offsetTop;
    const el_bottom = el_top + el.offsetHeight;
    return (el_top <= view_bottom) && (el_bottom >= view_top);
}

export default {
    closest,
    viewTop,
    inViewport,
};
