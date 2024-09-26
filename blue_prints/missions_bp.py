from flask import Blueprint, jsonify, request
from services.db_service import get_missions, get_missions_by_id


mission_bp = Blueprint('mission', __name__)

@mission_bp.route('/mission', methods=['GET'])
def get_mission():
    response = get_missions()
    # print(response)
    return (
        response
    ), 200



@mission_bp.route('/mission/<mission_id>', methods=['GET'])
def get_mission_by_mission_id(mission_id):
    mission_id = request.args.get('mission_id')
    response = get_missions_by_id(mission_id)
    return (
        response
    ), 200