import requests
import json
from functools import lru_cache

# Base URL for the API
BASE_URL = "https://psgc.gitlab.io/api"

@lru_cache(maxsize=32)
def get_regions():
    """Get all regions from the PSGC API"""
    url = f"{BASE_URL}/regions"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Sort by name
        data.sort(key=lambda x: x['name'])
        return data
    return []

@lru_cache(maxsize=32)
def get_provinces(region_code=None):
    """Get provinces from the PSGC API, optionally filtered by region code"""
    url = f"{BASE_URL}/provinces"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Filter by region if provided
        if region_code:
            data = [p for p in data if p.get('regionCode') == region_code]
        # Sort by name
        data.sort(key=lambda x: x['name'])
        return data
    return []

@lru_cache(maxsize=32)
def get_cities(province_code=None):
    """Get cities from the PSGC API, optionally filtered by province code"""
    url = f"{BASE_URL}/cities"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Filter by province if provided
        if province_code:
            data = [c for c in data if c.get('provinceCode') == province_code]
        # Sort by name
        data.sort(key=lambda x: x['name'])
        return data
    return []

@lru_cache(maxsize=32)
def get_municipalities(province_code=None):
    """Get municipalities from the PSGC API, optionally filtered by province code"""
    url = f"{BASE_URL}/municipalities"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Filter by province if provided
        if province_code:
            data = [m for m in data if m.get('provinceCode') == province_code]
        # Sort by name
        data.sort(key=lambda x: x['name'])
        return data
    return []

@lru_cache(maxsize=32)
def get_barangays(city_code=None, municipality_code=None):
    """Get barangays from the PSGC API, filtered by city or municipality code"""
    url = f"{BASE_URL}/barangays"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Filter by city or municipality
        if city_code:
            data = [b for b in data if b.get('cityCode') == city_code]
        elif municipality_code:
            data = [b for b in data if b.get('municipalityCode') == municipality_code]
        else:
            return []  # Too many to return without a filter
        # Sort by name
        data.sort(key=lambda x: x['name'])
        return data
    return []

def get_region_by_code(code):
    """Get a specific region by code"""
    regions = get_regions()
    for region in regions:
        if region['code'] == code:
            return region
    return None

def get_province_by_code(code):
    """Get a specific province by code"""
    provinces = get_provinces()
    for province in provinces:
        if province['code'] == code:
            return province
    return None

def get_city_by_code(code):
    """Get a specific city by code"""
    cities = get_cities()
    for city in cities:
        if city['code'] == code:
            return city
    return None

def get_municipality_by_code(code):
    """Get a specific municipality by code"""
    municipalities = get_municipalities()
    for municipality in municipalities:
        if municipality['code'] == code:
            return municipality
    return None

def get_barangay_by_code(code):
    """Get a specific barangay by code (requires full search)"""
    url = f"{BASE_URL}/barangays/{code}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None 