import os, tempfile
from datetime import date, timedelta
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from .config import MAX_UPLOAD_BYTES
from .database import get_db, init_db
from .hashing import sha256_file
from .reports import report_text, report_pdf

def row_dict(row): return dict(row) if row else None

def remove_temp(path):
    try:
        os.unlink(path)
    except OSError:
        pass

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_BYTES
    if test_config: app.config.update(test_config)
    CORS(app, resources={r'/api/*': {'origins': ['http://localhost:5173', 'http://127.0.0.1:5173']}})
    init_db(app.config.get('DATABASE_PATH'))

    def db(): return get_db(app.config.get('DATABASE_PATH'))
    def error(message, status=400): return jsonify({'error': message}), status
    def upload_file():
        file = request.files.get('file')
        if not file or not file.filename: return None, error('A file upload is required.')
        temp = tempfile.NamedTemporaryFile(prefix='securedoc_', suffix='.upload', delete=False)
        temp_path = temp.name
        temp.close()
        try:
            file.save(temp_path)
            if os.path.getsize(temp_path) > MAX_UPLOAD_BYTES:
                remove_temp(temp_path); return None, error('The upload exceeds the 100 MB limit.', 413)
            return (file, temp_path), None
        except OSError:
            remove_temp(temp_path)
            return None, error('The uploaded file could not be processed.', 422)

    @app.get('/api/health')
    def health(): return jsonify({'status':'ok','service':'SecureDoc API'})

    @app.get('/api/dashboard/stats')
    def stats():
        conn=db(); values = conn.execute("SELECT COUNT(*) documents, (SELECT COUNT(*) FROM verification_history WHERE result='MATCH') successful, (SELECT COUNT(*) FROM verification_history WHERE result='MISMATCH') failed, (SELECT COUNT(*) FROM verification_history) total FROM documents").fetchone(); conn.close(); return jsonify(dict(values))

    @app.get('/api/dashboard/recent-activity')
    def recent():
        conn=db(); rows=conn.execute('SELECT id, document_name, result, verified_at, calculated_hash FROM verification_history ORDER BY id DESC LIMIT 8').fetchall(); conn.close(); return jsonify({'items':[row_dict(r) for r in rows]})

    @app.get('/api/dashboard/chart')
    def chart():
        conn=db(); rows=conn.execute("SELECT substr(verified_at,1,10) day, SUM(result='MATCH') matches, SUM(result='MISMATCH') mismatches FROM verification_history WHERE result IN ('MATCH','MISMATCH') GROUP BY day ORDER BY day ASC").fetchall(); conn.close()
        if not rows: return jsonify({'items': []})
        counts={row['day']:{'matches':row['matches'] or 0,'mismatches':row['mismatches'] or 0} for row in rows}
        first=date.fromisoformat(rows[0]['day']); last=date.fromisoformat(rows[-1]['day']); items=[]; current=first
        while current <= last:
            day=current.isoformat(); items.append({'day':day, **counts.get(day, {'matches':0,'mismatches':0})}); current += timedelta(days=1)
        return jsonify({'items':items})

    @app.get('/api/documents')
    def documents():
        search=request.args.get('search','').strip(); page=max(request.args.get('page',1,type=int) or 1,1); per_page=min(max(request.args.get('per_page',10,type=int) or 10,1),50); sort=request.args.get('sort','created_at'); sort = sort if sort in {'name','created_at','size_bytes'} else 'created_at'; direction='ASC' if request.args.get('direction')=='asc' else 'DESC'; conn=db(); where='WHERE name LIKE ?' if search else ''; params=[f'%{search}%'] if search else []; total=conn.execute(f'SELECT COUNT(*) c FROM documents {where}',params).fetchone()['c']; rows=conn.execute(f'SELECT * FROM documents {where} ORDER BY {sort} {direction} LIMIT ? OFFSET ?',params+[per_page,(page-1)*per_page]).fetchall(); conn.close(); return jsonify({'items':[row_dict(r) for r in rows], 'total':total, 'page':page, 'per_page':per_page})

    @app.post('/api/documents/hash')
    def calculate_hash():
        uploaded, failure=upload_file()
        if failure: return failure
        file,path=uploaded
        try: return jsonify({'name':file.filename,'size_bytes':os.path.getsize(path),'mime_type':file.mimetype,'hash':sha256_file(path)})
        except OSError: return error('The uploaded file could not be processed.', 422)
        finally:
            remove_temp(path)

    @app.post('/api/documents')
    def register():
        uploaded,failure=upload_file()
        if failure: return failure
        file,path=uploaded
        try:
            try: digest=sha256_file(path)
            except OSError: return error('The uploaded file could not be processed.', 422)
            conn=db(); existing=conn.execute('SELECT id FROM documents WHERE name=? AND reference_hash=?',(file.filename,digest)).fetchone()
            if existing: conn.close(); return error('This document reference is already registered.',409)
            cur=conn.execute('INSERT INTO documents(name,reference_hash,size_bytes,mime_type) VALUES(?,?,?,?)',(file.filename,digest,os.path.getsize(path),file.mimetype)); conn.commit(); item=conn.execute('SELECT * FROM documents WHERE id=?',(cur.lastrowid,)).fetchone(); conn.close(); return jsonify(row_dict(item)),201
        finally:
            remove_temp(path)

    @app.get('/api/documents/<int:document_id>')
    def document_detail(document_id):
        conn=db(); item=conn.execute('SELECT * FROM documents WHERE id=?',(document_id,)).fetchone(); conn.close(); return jsonify(row_dict(item)) if item else error('Document not found.',404)

    @app.delete('/api/documents/<int:document_id>')
    def delete_document(document_id):
        conn=db(); cur=conn.execute('DELETE FROM documents WHERE id=?',(document_id,)); conn.commit(); conn.close(); return ('',204) if cur.rowcount else error('Document not found.',404)

    @app.post('/api/verify')
    def verify():
        document_id=request.form.get('document_id', type=int)
        if not document_id: return error('A registered document is required.')
        uploaded,failure=upload_file()
        if failure: return failure
        file,path=uploaded; conn=db(); document=conn.execute('SELECT * FROM documents WHERE id=?',(document_id,)).fetchone()
        if not document:
            conn.close()
            remove_temp(path)
            return error('Document not found.',404)
        try:
            try: current=sha256_file(path)
            except OSError: return error('The uploaded file could not be processed.', 422)
            result='MATCH' if current == document['reference_hash'] else 'MISMATCH'; cur=conn.execute('INSERT INTO verification_history(document_id,document_name,reference_hash,calculated_hash,result,file_size) VALUES(?,?,?,?,?,?)',(document_id,document['name'],document['reference_hash'],current,result,os.path.getsize(path))); conn.commit(); record=conn.execute('SELECT * FROM verification_history WHERE id=?',(cur.lastrowid,)).fetchone(); return jsonify(row_dict(record))
        finally:
            conn.close()
            remove_temp(path)

    @app.get('/api/history')
    def history():
        search=request.args.get('search','').strip(); result=request.args.get('result','').strip(); page=max(request.args.get('page',1,type=int),1); per_page=min(max(request.args.get('per_page',10,type=int),1),50); clauses=[]; params=[]
        if search: clauses.append('document_name LIKE ?'); params.append(f'%{search}%')
        if result in {'MATCH','MISMATCH','REFERENCE_NOT_FOUND'}: clauses.append('result=?'); params.append(result)
        where=('WHERE '+' AND '.join(clauses)) if clauses else ''; conn=db(); total=conn.execute(f'SELECT COUNT(*) c FROM verification_history {where}',params).fetchone()['c']; rows=conn.execute(f'SELECT * FROM verification_history {where} ORDER BY verified_at DESC LIMIT ? OFFSET ?',params+[per_page,(page-1)*per_page]).fetchall(); conn.close(); return jsonify({'items':[row_dict(r) for r in rows], 'total':total, 'page':page, 'per_page':per_page})

    @app.get('/api/history/<int:history_id>')
    def history_detail(history_id):
        conn=db(); item=conn.execute('SELECT * FROM verification_history WHERE id=?',(history_id,)).fetchone(); conn.close(); return jsonify(row_dict(item)) if item else error('Verification record not found.',404)

    @app.get('/api/reports/verification/<int:history_id>')
    def report(history_id):
        conn=db(); item=conn.execute('SELECT * FROM verification_history WHERE id=?',(history_id,)).fetchone(); conn.close()
        if not item: return error('Verification record not found.',404)
        fmt=request.args.get('format','txt').lower()
        if fmt=='pdf': return send_file(__import__('io').BytesIO(report_pdf(item)), mimetype='application/pdf', as_attachment=True, download_name=f'securedoc-report-{history_id}.pdf')
        if fmt=='txt': return send_file(__import__('io').BytesIO(report_text(item).encode()), mimetype='text/plain', as_attachment=True, download_name=f'securedoc-report-{history_id}.txt')
        return error('Report format must be txt or pdf.')

    @app.route('/api/settings', methods=['GET','PUT'])
    def settings():
        conn=db()
        if request.method=='PUT':
            values=request.get_json(silent=True) or {}; allowed={'app_name','max_upload_mb','retention_days'}
            for key,value in values.items():
                if key in allowed and str(value).strip(): conn.execute('INSERT OR REPLACE INTO settings(key,value) VALUES(?,?)',(key,str(value).strip()))
            conn.commit()
        rows=conn.execute('SELECT key,value FROM settings').fetchall(); conn.close(); return jsonify({r['key']:r['value'] for r in rows})

    @app.errorhandler(413)
    def too_large(_): return error('The upload exceeds the 100 MB limit.',413)
    return app

app=create_app()
if __name__ == '__main__': app.run(host='127.0.0.1', port=int(os.getenv('PORT',5000)), debug=False)
