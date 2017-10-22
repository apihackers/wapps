import VueRecaptcha from 'vue-recaptcha';
import {closest} from '../utils';

/**
 * Helpers for recaptcha enabled views/forms
 */
export default {
    components: {VueRecaptcha},
    methods: {
        onWappsFormsVerify(ref) {
            this.$refs[ref].submit();
        },
        onWappsFormsSubmit(ref, ev) {
            this.$refs[`${ref}-captcha`].execute();
        },
        onWappsFormsInvalid(ev) {
            closest(ev.target, '.form-group').classList.add('has-error');
        },
        onWappsFormsChange(ev) {
            const group = closest(ev.target, '.form-group');
            if (ev.target.checkValidity()) {
                group.classList.remove('has-error');
                group.classList.add('has-success');
            } else {
                group.classList.add('has-error');
                group.classList.remove('has-success');
            }
        }
    }
};
