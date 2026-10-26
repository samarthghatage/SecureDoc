import io, hashlib

def register(client, name='evidence.txt', content=b'original'):
    return client.post('/api/documents', data={'file':(io.BytesIO(content),name)}, content_type='multipart/form-data')

def test_register_and_verify_match(client):
    response=register(client); assert response.status_code == 201; doc=response.get_json(); assert doc['reference_hash'] == hashlib.sha256(b'original').hexdigest()
    result=client.post('/api/verify', data={'document_id':str(doc['id']),'file':(io.BytesIO(b'original'),'evidence.txt')}, content_type='multipart/form-data'); assert result.status_code == 200; assert result.get_json()['result']=='MATCH'

def test_modified_file_is_mismatch_and_history(client):
    doc=register(client).get_json(); result=client.post('/api/verify', data={'document_id':str(doc['id']),'file':(io.BytesIO(b'changed'),'evidence.txt')}, content_type='multipart/form-data'); assert result.get_json()['result']=='MISMATCH'; assert client.get('/api/history').get_json()['total']==1

def test_search_delete_preserves_history(client):
    doc=register(client).get_json(); client.post('/api/verify', data={'document_id':str(doc['id']),'file':(io.BytesIO(b'original'),'evidence.txt')}, content_type='multipart/form-data'); assert client.delete(f"/api/documents/{doc['id']}").status_code==204; assert client.get('/api/history').get_json()['total']==1

def test_reports(client):
    doc=register(client).get_json(); record=client.post('/api/verify', data={'document_id':str(doc['id']),'file':(io.BytesIO(b'original'),'evidence.txt')}, content_type='multipart/form-data').get_json(); assert b'MATCH' in client.get(f"/api/reports/verification/{record['id']}?format=txt").data; assert client.get(f"/api/reports/verification/{record['id']}?format=pdf").status_code==200
