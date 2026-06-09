import json
import requests
from threading import Lock
from utils.logger import logger
from pathlib import Path
from services.mirrors import get_all_mirrors

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

    resp = requests.get(url, params= {"q": package_name},timeout=3, allow_redirects=True)
    if resp.status_code < 400 :
        resp_data = resp.json()
        # Validation: check distro name
        if ("distro" in resp_data) and (distro == resp_data["distro"]):
            return True

    return False

def del_url_from_peer(distro, urls):
    """Remove existing peer's URLs in cache"""
    try:
        with peers_lock:
            if distro not in PEERS_CACHE:
                 return False
            current_data = PEERS_CACHE[distro]
            for url in urls:
                if url in current_data:
                    current_data.remove(url)
            
            PEERS_CACHE[distro] = current_data
            if current_data:
                logger.info(f"Updated peer: {distro} -> {current_data}")
                return True
    except Exception as e:
        logger.error(f"Error updating peer: {e}")
        return False

    # not current_data case
    return delete_peer(distro)

def add_url_to_peer(distro, urls):
    """Add existing peer's URLs in cache"""
    if distro not in PEERS_CACHE:
        return add_peer(distro, urls)

    try:
        with peers_lock:
            current_data = PEERS_CACHE[distro]
            for url in urls:
                if url not in current_data:
                    current_data.append(url)
            
            PEERS_CACHE[distro] = current_data
            logger.info(f"Updated peer: {distro} -> {current_data}")
            return True
    except Exception as e:
        logger.error(f"Error updating peer: {e}")
        return False

def add_peer(distro, urls):
    """Add a new dynamic peer to cache"""
    if distro not in get_all_mirrors():
        logger.error("Error adding peer (invalid distro)")
        return False

    try:
        with peers_lock:
            PEERS_CACHE[distro] = urls
            logger.info(f"Added peer: {distro} -> {urls}")
            return True
    except Exception as e:
        logger.error(f"Error adding peer: {e}")
        return False

def delete_peer(distro):
    """Delete a peer from the cache"""
    try:
        with peers_lock:
            if distro in PEERS_CACHE:
                del PEERS_CACHE[distro]
                
            logger.info(f"Deleted peer: {distro}")
            return True
    except Exception as e:
        logger.error(f"Error deleting peer: {e}")
        return False

def get_peers_management():
    """Get ALL peers for management UI"""
    with peers_lock:
        return PEERS_CACHE.copy()

