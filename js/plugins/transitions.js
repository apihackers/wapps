import Velocity from 'velocity-animate';

export function install(Vue) {
    Vue.transition('slide', {
        css: false,
        enter(el, done) {
            Velocity(el, 'transition.slideUpIn', 100, done);
        },
        leave(el, done) {
            Velocity(el, 'transition.slideUpOut', 200, done);
        }
    });

    Vue.transition('fade', {
        css: false,
        enter(el, done) {
            Velocity(el, 'fadeIn', 500, done);
        },
        leave(el, done) {
            Velocity(el, 'fadeOut', 500, done);
        }
    });
}
