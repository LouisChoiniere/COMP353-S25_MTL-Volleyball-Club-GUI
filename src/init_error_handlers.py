from flask import render_template
from sqlalchemy.exc import OperationalError, IntegrityError

def init_error_handlers(app):
    @app.errorhandler(OperationalError)
    def handle_operational_error(error):

        # Check if this is actually a trigger violation (SQLSTATE 45000)
        if hasattr(error.orig, 'args') and len(error.orig.args) >= 1:
            if error.orig.args[0] == 1644: # MySQL error code for SIGNAL SQLSTATE '45000'
                return handle_integrity_error(error)

        return render_template('errors/database_error.html', error=error), 500

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        return render_template('errors/business_rule_violation.html', error=error), 400