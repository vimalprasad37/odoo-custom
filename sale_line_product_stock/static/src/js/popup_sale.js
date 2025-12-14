/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { Dialog } from "@web/core/dialog/dialog";

const { Component, useExternalListener, onMounted } = owl;

patch(Dialog.prototype,'/sale_line_product_stock/static/src/js/popup_sale.js',{
    setup() {
        this._super.apply();
        onMounted(this.mount)
    },

    mount(){
        const treeView = document.querySelector('.o_tree_view_custom');
        if (treeView) {
            const modalDialog = document.querySelector('.modal-dialog');
            const modalContent = document.querySelector('.modal-content');
            const modalBody = document.querySelector('.modal-body');

            if (modalDialog) {
                modalDialog.style.maxWidth = '98%';
                modalDialog.style.height = '99%';
            }
            if (modalContent) {
                modalContent.style.maxWidth = '100%';
                modalContent.style.height = '100%';
            }
            if (modalBody) {
                modalBody.style.height = '100%';
            }
        }
    },
});