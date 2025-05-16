/** tender_dashboard.js **/
/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class TenderDashboard extends Component {
    setup() {
        console.log("TenderDashboard component loaded!");
    }

    static template = "tender_pro.TenderDashboard";
}

// Register the component
registry.category("actions").add("tender_dashboard_widget", TenderDashboard);
