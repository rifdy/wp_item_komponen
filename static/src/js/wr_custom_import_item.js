odoo.define('warungpintar_item_komponen.custom_import_button', function (require) {
"use strict";
var core = require('web.core');
var ListController = require('web.ListController');
    ListController.include({
        renderButtons: function($node) {
        this._super.apply(this, arguments);
            if (this.$buttons) {
                let custom_import_button = this.$buttons.find('.oe_cust_import_button');
                custom_import_button && custom_import_button.click(this.proxy('custom_import_button'));
            }
        },
        custom_import_button: function () {
            this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'wr.item.import',
                view_mode: 'form',
                view_type: 'form',
                views: [[false, 'form']],
                target: 'new',
                context:{}
            });
        }

    });

});