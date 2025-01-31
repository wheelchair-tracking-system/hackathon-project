from flask import Flask, render_template, request, jsonify, session, url_for, flash, redirect, Response
import serial
import time
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


@app.route('/gpspage')
def gpspage():
    return render_template('gps.html')

@app.route('/gps')
def gps():
    ser = serial.Serial('COM9', 9600, timeout=1)
    def generate_gps_data():
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                try:
                    yield f"data: {data}\n\n"
                except ValueError:
                    pass 
                time.sleep(4)
    return Response(generate_gps_data(), mimetype='text/event-stream')


app.secret_key = 'efojo' 
app.config['SESSION_TYPE'] = 'filesystem' 
Session(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('register'))
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists')
            return redirect(url_for('register'))
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully')
    return redirect('/')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Mock data for wheelchairs
wheelchairs = [
    {"id": 1, "status": "available", "patient_id": None},
    {"id": 2, "status": "available", "patient_id": None},
    {"id": 3, "status": "available", "patient_id": None},
    {"id": 4, "status": "in_use", "patient_id": "P1002"},
    {"id": 5, "status": "in_use", "patient_id": "P1003"},
    {"id": 6, "status": "under_maintenance", "patient_id": None, "problem": "Flat Tire"},
    {"id": 7, "status": "available", "patient_id": None},
    {"id": 8, "status": "available", "patient_id": None},
    {"id": 9, "status": "in_use", "patient_id": "P1004"},
    {"id": 10, "status": "available", "patient_id": None},
    {"id": 11, "status": "under_maintenance", "patient_id": None},
    {"id": 12, "status": "available", "patient_id": None},
    {"id": 13, "status": "available", "patient_id": None},
    {"id": 14, "status": "in_use", "patient_id": "P1005"},
    {"id": 15, "status": "available", "patient_id": None},
    {"id": 16, "status": "available", "patient_id": None},
    {"id": 17, "status": "in_use", "patient_id": "P1006"},
    {"id": 18, "status": "under_maintenance", "patient_id": None},
    {"id": 19, "status": "available", "patient_id": None},
    {"id": 20, "status": "available", "patient_id": None},
    {"id": 21, "status": "available", "patient_id": None},
    {"id": 22, "status": "in_use", "patient_id": "P1007"},
    {"id": 23, "status": "available", "patient_id": None},
    {"id": 24, "status": "under_maintenance", "patient_id": None, "problem": "Broken Armrest"},
    {"id": 25, "status": "available", "patient_id": None},
    {"id": 26, "status": "in_use", "patient_id": "P1008"},
    {"id": 27, "status": "available", "patient_id": None},
    {"id": 28, "status": "under_maintenance", "patient_id": None},
    {"id": 29, "status": "available", "patient_id": None},
    {"id": 30, "status": "in_use", "patient_id": "P1009"},
    {"id": 31, "status": "available", "patient_id": None},
    {"id": 32, "status": "under_maintenance", "patient_id": None, "problem": "Loose Wheel"},
    {"id": 33, "status": "available", "patient_id": None},
    {"id": 34, "status": "in_use", "patient_id": "P1010"},
    {"id": 35, "status": "available", "patient_id": None},
    {"id": 36, "status": "available", "patient_id": None},
    {"id": 37, "status": "in_use", "patient_id": "P1011"},
    {"id": 38, "status": "under_maintenance", "patient_id": None},
    {"id": 39, "status": "available", "patient_id": None},
    {"id": 40, "status": "available", "patient_id": None},
    {"id": 41, "status": "available", "patient_id": None},
    {"id": 42, "status": "in_use", "patient_id": "P1012"},
    {"id": 43, "status": "available", "patient_id": None},
    {"id": 44, "status": "under_maintenance", "patient_id": None, "problem": "Damaged Frame"},
    {"id": 45, "status": "available", "patient_id": None},
    {"id": 46, "status": "in_use", "patient_id": "P1013"},
    {"id": 47, "status": "available", "patient_id": None},
    {"id": 48, "status": "under_maintenance", "patient_id": None},
    {"id": 49, "status": "available", "patient_id": None},
    {"id": 50, "status": "in_use", "patient_id": "P1014"},
    {"id": 51, "status": "available", "patient_id": None},
    {"id": 52, "status": "under_maintenance", "patient_id": None, "problem": "Faulty Brake"},
    {"id": 53, "status": "available", "patient_id": None},
    {"id": 54, "status": "in_use", "patient_id": "P1015"},
    {"id": 55, "status": "available", "patient_id": None},
    {"id": 56, "status": "available", "patient_id": None},
    {"id": 57, "status": "in_use", "patient_id": "P1016"},
    {"id": 58, "status": "under_maintenance", "patient_id": None},
    {"id": 59, "status": "available", "patient_id": None},
    {"id": 60, "status": "available", "patient_id": None},
    {"id": 61, "status": "available", "patient_id": None},
    {"id": 62, "status": "in_use", "patient_id": "P1017"},
    {"id": 63, "status": "available", "patient_id": None},
    {"id": 64, "status": "under_maintenance", "patient_id": None, "problem": "Wheel Misalignment"},
    {"id": 65, "status": "available", "patient_id": None},
    {"id": 66, "status": "in_use", "patient_id": "P1018"},
    {"id": 67, "status": "available", "patient_id": None},
    {"id": 68, "status": "under_maintenance", "patient_id": None},
    {"id": 69, "status": "available", "patient_id": None},
    {"id": 70, "status": "in_use", "patient_id": "P1019"},
    {"id": 71, "status": "available", "patient_id": None},
    {"id": 72, "status": "under_maintenance", "patient_id": None, "problem": "Seat Tear"},
    {"id": 73, "status": "available", "patient_id": None},
    {"id": 74, "status": "in_use", "patient_id": "P1020"},
    {"id": 75, "status": "available", "patient_id": None},
    {"id": 76, "status": "available", "patient_id": None},
    {"id": 77, "status": "in_use", "patient_id": "P1021"},
    {"id": 78, "status": "under_maintenance", "patient_id": None},
    {"id": 79, "status": "available", "patient_id": None},
    {"id": 80, "status": "available", "patient_id": None},
    {"id": 81, "status": "available", "patient_id": None},
    {"id": 82, "status": "in_use", "patient_id": "P1022"},
    {"id": 83, "status": "available", "patient_id": None},
    {"id": 84, "status": "under_maintenance", "patient_id": None, "problem": "Broken Footrest"},
    {"id": 85, "status": "available", "patient_id": None},
    {"id": 86, "status": "in_use", "patient_id": "P1023"},
    {"id": 87, "status": "available", "patient_id": None},
    {"id": 88, "status": "under_maintenance", "patient_id": None},
    {"id": 89, "status": "available", "patient_id": None},
    {"id": 90, "status": "in_use", "patient_id": "P1024"},
    {"id": 91, "status": "available", "patient_id": None},
    {"id": 92, "status": "under_maintenance", "patient_id": None, "problem": "Rusty Frame"},
    {"id": 93, "status": "available", "patient_id": None},
    {"id": 94, "status": "in_use", "patient_id": "P1025"},
    {"id": 95, "status": "available", "patient_id": None},
    {"id": 96, "status": "available", "patient_id": None},
    {"id": 97, "status": "in_use", "patient_id": "P1026"},
    {"id": 98, "status": "under_maintenance", "patient_id": None},
    {"id": 99, "status": "available", "patient_id": None},
    {"id": 100, "status": "available", "patient_id": None}
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/wheelchairs', methods=['GET'])
def get_wheelchairs():
    available = sum(1 for w in wheelchairs if w['status'] == 'available')
    in_use = sum(1 for w in wheelchairs if w['status'] == 'in_use')
    return jsonify({"available": available, "in_use": in_use, "data": wheelchairs})

@app.route('/api/wheelchairs/in_use', methods=['GET'])
def get_in_use_wheelchairs():
    in_use_wheelchairs = [w for w in wheelchairs if w['status'] == 'in_use']
    return jsonify(in_use_wheelchairs)

@app.route('/wheelchairdispense')
def wheelchairdispense():
    return render_template('wheelchairdispense.html')

@app.route('/api/dispense', methods=['POST'])
def dispense_wheelchair():
    data = request.json
    patient_id = data.get("patient_id")

    # Find the next available wheelchair
    for wheelchair in wheelchairs:
        if wheelchair["status"] == "available":
            wheelchair["status"] = "in_use"
            wheelchair["patient_id"] = patient_id
            return jsonify({"success": True, "message": f"Wheelchair {wheelchair['id']} assigned to patient {patient_id}"})

    return jsonify({"success": False, "message": "No wheelchairs available"})

@app.route('/return-wheelchair', methods=['GET'])
def return_wheelchair_page():
    return render_template('return_wheelchair.html')

@app.route('/api/return', methods=['POST'])
def return_wheelchair():
    data = request.json
    wheelchair_id = data.get("wheelchair_id")

    for wheelchair in wheelchairs:
        if wheelchair["id"] == int(wheelchair_id) and wheelchair["status"] == "in_use":
            wheelchair["status"] = "available"
            wheelchair["patient_id"] = None
            return jsonify({"success": True, "message": f"Wheelchair {wheelchair_id} returned successfully."})

    return jsonify({"success": False, "message": "Invalid wheelchair ID or wheelchair not in use."})

@app.route('/complaint')
def complaint_page():
    return render_template('complaint_page.html')

@app.route('/admin/maintenance')
def admin_maintenance():
    return render_template('admin_maintenance.html')

@app.route('/api/mark_repaired', methods=['POST'])
def mark_repaired():
    data = request.json
    wheelchair_id = data.get('wheelchair_id')

    if not wheelchair_id:
        return jsonify({'message': 'Missing wheelchair ID'}), 400

    wheelchair = next((w for w in wheelchairs if w['id'] == wheelchair_id), None)

    if wheelchair:
        wheelchair['status'] = 'available'
        wheelchair.pop('problem', None)  # Remove problem field when repaired
        return jsonify({'message': f'Wheelchair {wheelchair_id} marked as available'}), 200
    else:
        return jsonify({'message': 'Wheelchair not found'}), 404

@app.route('/api/report_complaint', methods=['POST'])
def report_complaint():
    data = request.json
    wheelchair_id = data.get('wheelchair_id')
    problem = data.get('problem')

    if not wheelchair_id or not problem:
        return jsonify({'message': 'Missing wheelchair ID or problem'}), 400

    wheelchair = next((w for w in wheelchairs if str(w['id']) == str(wheelchair_id)), None)

    if wheelchair:
        if wheelchair['status'] == 'under_maintenance':
            return jsonify({'message': 'This wheelchair is already under maintenance'}), 400
        
        wheelchair['status'] = 'under_maintenance'
        wheelchair['problem'] = problem

        return jsonify({'message': 'Complaint reported successfully and wheelchair marked as under maintenance'}), 200
    else:
        return jsonify({'message': 'Wheelchair not found'}), 404


@app.route('/api/under_maintenance', methods=['GET'])
def under_maintenance():
    maintenance_wheelchairs = [w for w in wheelchairs if w['status'] == 'under_maintenance']
    return jsonify(maintenance_wheelchairs)

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/credit')
def credit():
    return render_template('creditsandcode.html')

emergency_requests = []

@app.route('/wheelchairdispense/emergency')
def emergency():
    return render_template('emergency_request.html')

@app.route('/admin/requests')
def admin_panel():
    return render_template('admin_panel.html', requests=emergency_requests)

@app.route('/admin')
def admin():
    return render_template('admin_dashboard.html')

@app.route('/api/emergency_request', methods=['POST'])
def submit_request():
    data = request.json
    if not data.get('staff_id') or not data.get('location'):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400

    emergency_requests.append({
        'staff_id': data['staff_id'],
        'location': data['location'],
        'notes': data.get('notes', ''),
        'status': 'Pending'
    })
    
    return jsonify({'success': True, 'message': 'Request submitted successfully'})

@app.route('/api/requests', methods=['GET'])
def get_requests():
    return jsonify(emergency_requests)

@app.route('/api/update_status', methods=['POST'])
def update_status():
    data = request.json
    request_index = data.get('index')
    new_status = data.get('status')

    if request_index is not None and 0 <= request_index < len(emergency_requests):
        if new_status in ['Approved', 'Declined']:
            emergency_requests[request_index]['status'] = new_status
            return jsonify({'success': True, 'message': 'Status updated successfully'})
    
    return jsonify({'success': False, 'message': 'Invalid request'}), 400

@app.route('/admin/wheelchair_status')
def wheelchair_status():
    return render_template('wheelchair_status.html')

if __name__ == '__main__':
    app.run(debug=True)