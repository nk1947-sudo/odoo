from odoo import api, SUPERUSER_ID

# post_init.py
def post_init_remove_broken_report(env):
    """
    This post-init hook removes broken 'work.report.export' model records.
    """
    env.cr.execute("DELETE FROM ir_model WHERE model = 'work.report.export'")
    env.cr.execute("""
        DELETE FROM ir_model_access 
        WHERE model_id IN (
            SELECT id FROM ir_model WHERE model = 'work.report.export'
        )
    """)
    # Check if ir_actions_report table exists before deleting
    env.cr.execute("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables 
            WHERE table_name='ir_actions_report'
        )
    """)
    if env.cr.fetchone()[0]:
        env.cr.execute("DELETE FROM ir_actions_report WHERE model = 'work.report.export'")

