<template>
<div class="slideout-container">
    <div class="over-page" :class="{open: isOpening || isOpen}" @click="close"></div>
    <div ref="menu" class="slideout-menu">
        <slot name="menu" />
    </div>
    <div ref="panel" class="slideout-panel" @click="onPanelClick($event)">
        <slot />
    </div>
</div>
</template>
<script>
import Slideout from 'slideout';

const DEFAULT_MOBILE_MENU_WIDTH = 295;

export default {
    data() {
        return {
            isOpening: false,
            isOpen: false,
            slideout: null,
        };
    },
    props: {
        width: {type: Number, default: DEFAULT_MOBILE_MENU_WIDTH},
    },
    mounted() {
        // navigation custom Slideout.js
        const slideout = this.slideout = new Slideout({
            'panel': this.$refs.panel,
            'menu': this.$refs.menu,
            'padding': this.width,
            'tolerance': 70,
            'touch': false
        });

        this.toReset = [...document.querySelectorAll('.panel-menu-content, .panel-list-level')];

        // push content
        slideout.on('beforeopen', () => this.isOpening = true);
        slideout.on('open', () => {
            this.isOpen = true;
            this.isOpening = false;
        });
        slideout.on('close', () => this.isOpen = false);
    },
    methods: {
        toggle() {
            this.slideout.toggle();
        },
        open() {
            this.slideout.open();
        },
        close() {
            if (this.isOpen) {
                this.slideout.close();
                this.toReset.forEach(el => el.classList.remove('open'));
            }
        },
        onPanelClick(event) {
            if (this.isOpen) {
                this.close();
                event.preventDefault();
                event.stopPropagation();
            }
        }
    }
};
</script>
<style lang="scss">
.slideout-container {
    .slideout-menu {

    }

    .slideout-panel {

    }
}
</style>
