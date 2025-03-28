/** @odoo-module **/

import { session } from '@web/session';
import { patch } from '@web/core/utils/patch';
import { onMounted, onWillUnmount, onPatched, useRef, useEffect, useState } from '@odoo/owl';
import { ScrollTopButton } from '@eist_web_theme/components/scroll_top_button/scroll_top_button';
import { SettingsPage } from '@web/webclient/settings_form_view/settings/settings_page';

patch(SettingsPage.prototype, {

	setup() {
		super.setup(...arguments);
		this.offset = 300;
		this.theme = session.theme;
		this.displayScrollTopButton = this.theme["views"]["display_scroll_top_button"];
		this.state.show = false

		this.onScrollSettingsEl = (ev) => {
			if (this.displayScrollTopButton) {
				if (ev.target.scrollTop > this.offset) {
					// this.scrollTopButton.classList.remove('o_hidden');
					this.state.show = true;
				} else {
					// this.scrollTopButton.classList.add('o_hidden');
					this.state.show = false;
				}
			}
		}

		onMounted(() => {
			this.scrollTopButton = this.settingsRef.el.parentElement.querySelector('.o_scroll_top');

			this.settingsRef.el.addEventListener('scroll', this.onScrollSettingsEl);
		});
	},

})

SettingsPage.components = {
	...SettingsPage.components,
	ScrollTopButton,
};