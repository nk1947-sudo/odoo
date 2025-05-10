/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class WorkReportDashboard extends Component {
    setup() {
        this.state = useState({
            message: "Welcome to the Work Report Dashboard!",
        });
    }

    static template = "work_report_module.WorkReportDashboard";
}

registry.category("actions").add("work_report_dashboard", WorkReportDashboard);
