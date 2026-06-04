import json
import requests
from threading import Lock
from utils.logger import logger
from pathlib import Path

# In-memory support for peers
# Structure: {'distro': [urls ...]}

PEERS_CACHE = {} 
peers_lock = Lock()

def get_peers_urls(distro, package_path):
    """Get urls of peers where package is already cached"""
    valid_urls = []
    package_name=Path(package_path).stem
    # Validation: Check distro availability in peers list
    if distro in PEERS_CACHE:
        for url in PEERS_CACHE[distro]:
            # Validation: Check if url is reachable and the availability of tne package in remote cache
            if validate_peer(url, distro, package_name):
                valid_urls.append(url)

    return valid_urls

def validate_peer(url, distro, package_name):
    """Check if the peer URL is reachable and package is available from peers cache"""

    resp = requests.get(url, params= {"q": package_name},timeout=5, allow_redirects=True)
    if resp.status_code < 400 :
        resp_data = resp.json()
        # Validation: check distro name
        if ("distro" in resp_data) and (distro == resp_data["distro"]):
            return True

    return False

def add_peer(distro, urls):
    """Add a new dynamic peer to cache"""

    try:
        with peers_lock:
            PEERS_CACHE[distro] = urls
            logger.info(f"Added peer: {name} -> {urls}")
            return True
    except Exception as e:
        logger.error(f"Error adding peer: {e}")
        return False

def update_peer(distro, urls=None):
    """Update an existing peer's URLs in cache"""
    try:
        with peers_lock:
            if distro not in PEERS_CACHE:
                 return False
            current_data = PEERS_CACHE[distro]
            
            new_urls = urls if urls is not None else current_data['urls']
        
            PEERS_CACHE[distro] = new_urls
            logger.info(f"Updated peer: {distro} -> {new_urls}")
            return True
    except Exception as e:
        logger.error(f"Error updating peer: {e}")
        return False

def delete_peer(distro):
    """Delete a peer from the cache"""
    try:
        with peers_lock:
            if distro in PEERS_CACHE:
                del PEERS_CACHE[name]
                
            logger.info(f"Deleted peer: {name}")
            return True
    except Exception as e:
        logger.error(f"Error deleting peer: {e}")
        return False

