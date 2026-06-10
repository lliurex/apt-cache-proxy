from flask import Blueprint, Response, request, jsonify
from utils.routes  import check_auth
from services.peers import get_all_peers, add_url_to_peer, del_url_from_peer
from services.mirrors import get_all_mirrors

routes_peers = Blueprint('routes_peers', __name__)

@routes_peers.route('/api/peers', methods=['GET'])
def api_peers():
    """Get peers list"""
    return jsonify(get_all_peers())

@routes_peers.route('/api/peers/<name>', methods=['PUT'])
def api_add_peers(name):
    """Add/update peers URLs"""
    if not check_auth():
        return Response("Unauthorized", status=401)
        
    data = request.get_json()
    urls = data.get('urls')
    
    if add_url_to_peer(name, urls=urls):
        return jsonify({'status': 'success'})
    return Response("Failed to add peer URL", status=500)

@routes_peers.route('/api/peers/<name>', methods=['DELETE'])
def api_del_peers(name):
    """Delete peers URLs"""
    if not check_auth():
        return Response("Unauthorized", status=401)
        
    data = request.get_json()
    urls = data.get('urls')
    
    if del_url_from_peer(name, urls=urls):
        return jsonify({'status': 'success'})
    return Response("Failed to delete peer URL", status=500)

@routes_peers.route('/api/mirrors', methods=['GET'])
def api_mirrors():
    """Get all mirrors with status for admin panel"""
    return jsonify(get_all_mirrors())


