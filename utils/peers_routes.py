from flask import Blueprint, Response, request, jsonify
from utils.routes  import check_auth
from services.peers import get_peers_management, add_url_to_peer, del_url_from_peer

routes_peers = Blueprint('routes_peers', __name__)

@routes_peers.route('/api/peers', methods=['GET'])
def api_peers():
    """Get all mirrors with status for admin panel"""
    if not check_auth():
        return Response("Unauthorized", status=401)
    return jsonify(get_peers_management())

@routes_peers.route('/api/peers/<name>', methods=['PUT'])
def api_add_peers(name):
    """Add/update peers URLs"""
    if not check_auth():
        return Response("Unauthorized", status=401)
        
    data = request.get_json()
    urls = data.get('urls')
    
    if add_url_to_peer(name, urls=urls):
        return jsonify({'status': 'success'})
    return Response("Failed to add èer URL", status=500)

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
