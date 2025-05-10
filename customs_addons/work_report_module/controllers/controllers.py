from odoo import http
from odoo.http import request
import json
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)
_logger.info("🚀 work.report.template model loaded successfully.")
class WorkReportController(http.Controller):

    @http.route('/api/work_report', type='http', auth='user', methods=['GET'], csrf=False)
    def get_work_reports(self, **kwargs):
        try:
            domain = []
            if 'date_from' in kwargs:
                datetime.strptime(kwargs['date_from'], '%Y-%m-%d')
                domain.append(('date', '>=', kwargs['date_from']))
            if 'date_to' in kwargs:
                datetime.strptime(kwargs['date_to'], '%Y-%m-%d')
                domain.append(('date', '<=', kwargs['date_to']))
            if 'employee_id' in kwargs:
                employee_id = int(kwargs['employee_id'])
                domain.append(('employee_id', '=', employee_id))
            if 'state' in kwargs:
                domain.append(('state', '=', kwargs['state']))
            reports = request.env['work.report'].search(domain)
            result = []
            for report in reports:
                result.append({
                    'id': report.id,
                    'name': report.name,
                    'date': str(report.date),
                    'employee_id': report.employee_id.id,
                    'employee_name': report.employee_id.name,
                    'total_hours': report.total_hours,
                    'billable_hours': report.billable_hours,
                    'state': report.state,
                })
            return http.Response(json.dumps(result), content_type='application/json', status=200)
        except Exception as e:
            return self._error_response(500, str(e))

    @http.route('/api/work_report/<int:report_id>', type='http', auth='user', methods=['GET'], csrf=False)
    def get_work_report(self, report_id, **kwargs):
        try:
            report = request.env['work.report'].browse(report_id)
            if not report.exists():
                return self._error_response(404, "Report not found.")
            report_data = {
                'id': report.id,
                'name': report.name,
                'date': str(report.date),
                'employee_id': report.employee_id.id,
                'employee_name': report.employee_id.name,
                'total_hours': report.total_hours,
                'billable_hours': report.billable_hours,
                'state': report.state,
                'lines': [
                    {
                        'id': line.id,
                        'name': line.name,
                        'project_id': line.project_id.id if line.project_id else False,
                        'project_name': line.project_id.name if line.project_id else '',
                        'task_id': line.task_id.id if line.task_id else False,
                        'task_name': line.task_id.name if line.task_id else '',
                        'hours': line.hours,
                        'billable': line.billable,
                    } for line in report.line_ids
                ]
            }
            return http.Response(json.dumps(report_data), content_type='application/json', status=200)
        except Exception as e:
            return self._error_response(500, str(e))

    @http.route('/api/work_report', type='json', auth='user', methods=['POST'], csrf=False)
    def create_work_report(self, **kwargs):
        try:
            data = request.jsonrequest
            required_fields = ['date', 'employee_id']
            for field in required_fields:
                if field not in data or not data[field]:
                    return {'success': False, 'error': f"Missing or empty field: {field}"}
            report = request.env['work.report'].create({
                'date': data['date'],
                'employee_id': int(data['employee_id']),
                'reference': data.get('reference', ''),
                'notes': data.get('notes', ''),
            })
            for line in data.get('lines', []):
                try:
                    request.env['work.report.line'].create({
                        'report_id': report.id,
                        'name': line['name'],
                        'hours': float(line['hours']),
                        'project_id': int(line['project_id']) if line.get('project_id') else False,
                        'task_id': int(line['task_id']) if line.get('task_id') else False,
                        'billable': bool(line.get('billable', True)),
                    })
                except Exception as line_e:
                    _logger.exception("Failed to create work report line: %s", line)
                    return {'success': False, 'error': f"Line error: {str(line_e)}"}
            return {'success': True, 'id': report.id, 'name': report.name}
        except Exception as e:
            _logger.exception("Failed to create work report")
            return {'success': False, 'error': str(e)}

    def _error_response(self, status, message):
        return http.Response(json.dumps({'error': message}), content_type='application/json', status=status)

class FileUploadController(http.Controller):

    @http.route('/my_module/upload', type='http', auth='user', methods=['POST'], csrf=True)
    def upload_file(self, **kwargs):
        file = kwargs.get('file')
        if not file:
            return request.make_response(json.dumps({'error': 'No file uploaded.'}), status=400, headers=[('Content-Type', 'application/json')])
        try:
            filename = getattr(file, 'filename', '')
            if not filename.lower().endswith(('.csv', '.xlsx', '.xls', '.txt')):
                return request.make_response(json.dumps({'error': 'Unsupported file type.'}), status=415, headers=[('Content-Type', 'application/json')])
            file.seek(0, 2)
            size = file.tell()
            if size > 5 * 1024 * 1024:
                return request.make_response(json.dumps({'error': 'File too large (max 5MB).'}), status=413, headers=[('Content-Type', 'application/json')])
            file.seek(0)
            try:
                content = file.read().decode('utf-8')
            except UnicodeDecodeError:
                _logger.error("File encoding error: not UTF-8")
                return request.make_response(json.dumps({'error': 'File encoding must be UTF-8.'}), status=415, headers=[('Content-Type', 'application/json')])
            # Process file...
            return request.make_response(json.dumps({'success': True, 'message': 'File uploaded successfully.'}), status=200, headers=[('Content-Type', 'application/json')])
        except Exception as e:
            _logger.exception("Unexpected error during file upload")
            return request.make_response(json.dumps({'error': f'Upload failed: {str(e)}'}), status=500, headers=[('Content-Type', 'application/json')])