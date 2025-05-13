/** tender_dashboard.js **/

odoo.define('dawell_tender_pro.dashboard', function (require) {
    "use strict";

    const publicWidget = require('web.public.widget');

    publicWidget.registry.TenderKPIDashboard = publicWidget.Widget.extend({
        selector: '.o_dashboard',
        start: function () {
            console.log("Tender Dashboard Widget Loaded.");
            this._renderKPIStats();
        },

        _renderKPIStats: function () {
            // Example logic — in practice this would fetch from server or model
            const kpis = [
                { title: "Active Tenders", value: "42", footer: "Updated today" },
                { title: "Submitted Bids", value: "18", footer: "This month" },
                { title: "Win Rate", value: "68%", footer: "Last 30 days" },
                { title: "Pending Deadlines", value: "9", footer: "Next 7 days" },
            ];

            const container = this.$el;
            container.empty();

            kpis.forEach(kpi => {
                const card = $(`
                    <div class="kpi-card">
                        <div class="kpi-title">${kpi.title}</div>
                        <div class="kpi-value">${kpi.value}</div>
                        <div class="kpi-footer">${kpi.footer}</div>
                    </div>
                `);
                container.append(card);
            });
        }
    });
});
