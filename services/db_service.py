from flask import jsonify
from models.models import Mission, TargetDetails, Location, Coordinates

def get_missions():
    missions = Mission.query.all()
    mission_list = []

    for mission in missions[:10]:
        mission_data = {
            'mission_id': mission.mission_id,
            'target': {
                'target_id': mission.target.target_id,
                'target_type': mission.target.target_type,
                'target_industry': mission.target.target_industry,
                'target_priority': mission.target.target_priority,
                'location': {
                    'country': mission.target.location.country,
                    'city': mission.target.location.city
                },
                'coordinates': {
                    'latitude': mission.target.coordinates.latitude,
                    'longitude': mission.target.coordinates.longitude
                }
            }
        }
        mission_list.append(mission_data)
    print(mission_list)
    return jsonify(mission_list)

def get_missions_by_id(mission_id):
    mission = Mission.query.filter_by(mission_id=mission_id).first()
    mission_data = {
        'mission_id': mission.mission_id,
        'target': {
            'target_id': mission.target.target_id,
            'target_type': mission.target.target_type,
            'target_industry': mission.target.target_industry,
            'target_priority': mission.target.target_priority,
            'location': {
                'country': mission.target.location.country,
                'city': mission.target.location.city
            },
            'coordinates': {
                'latitude': mission.target.coordinates.latitude,
                'longitude': mission.target.coordinates.longitude
            }
        }
    }
    return jsonify(mission_data)