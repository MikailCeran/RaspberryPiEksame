from flask import Flask, jsonify, request
from datetime import datetime
import json

app = Flask(__name__)

class NoiseMeter:
    def __init__(self, id, date, db_volume, unit, is_occupied):
        self.Id = id
        self.Date = date
        self.DbVolume = db_volume
        self.Unit = unit
        self.IsOccupied = is_occupied

    def __repr__(self):
        return f"NoiseMeter(Id={self.Id}, Date={self.Date}, DbVolume={self.DbVolume}, Unit={self.Unit}, IsOccupied={self.IsOccupied})"

class NoiseMeterRepository:
    noise_meter_list = []

    @staticmethod
    def get_next_id():
        if not NoiseMeterRepository.noise_meter_list:
            return 1

        max_id = max(n.Id for n in NoiseMeterRepository.noise_meter_list)
        return max_id + 1

    @staticmethod
    def add_noise_meter(date, db_volume, unit, is_occupied):
        new_noise_meter = NoiseMeter(
            NoiseMeterRepository.get_next_id(),
            date,
            db_volume,
            unit,
            is_occupied
        )
        NoiseMeterRepository.noise_meter_list.append(new_noise_meter)

    @staticmethod
    def get_all():
        return NoiseMeterRepository.noise_meter_list

    @staticmethod
    def get_max_volume():
        if not NoiseMeterRepository.noise_meter_list:
            raise ValueError("The list is empty. Cannot find max volume.")

        return max(NoiseMeterRepository.noise_meter_list, key=lambda n: float(n.DbVolume))

    @staticmethod
    def filter_by_date(start_date, end_date):
        return [n for n in NoiseMeterRepository.noise_meter_list if start_date <= n.Date <= end_date]

    @staticmethod
    def is_room_occupied(threshold_db_volume):
        return any(float(n.DbVolume) > threshold_db_volume for n in NoiseMeterRepository.noise_meter_list)

    @staticmethod
    def update_all(updated_noise_meters):
        NoiseMeterRepository.noise_meter_list = updated_noise_meters

@app.route('/update_all', methods=['POST'])
def update_all():
    try:
        data = request.json
        updated_noise_meters = [NoiseMeter(**item) for item in data]
        NoiseMeterRepository.update_all(updated_noise_meters)
        return jsonify({"message": "Data updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/is_room_occupied', methods=['GET'])
def is_room_occupied():
    try:
        threshold = float(request.args.get('threshold', 0.0))
        result = NoiseMeterRepository.is_room_occupied(threshold)
        return jsonify({"is_room_occupied": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/filter_by_date', methods=['GET'])
def filter_by_date():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        result = [n.__dict__ for n in NoiseMeterRepository.filter_by_date(start_date, end_date)]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_max_volume', methods=['GET'])
def get_max_volume():
    try:
        max_volume = NoiseMeterRepository.get_max_volume()
        return jsonify(max_volume.__dict__)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_all', methods=['GET'])
def get_all():
    try:
        all_data = [n.__dict__ for n in NoiseMeterRepository.get_all()]
        return jsonify(all_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
