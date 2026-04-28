from flask import Flask, render_template, redirect, url_for, request, flash
from model import db, Patient, MedicalHistory, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, redirect, url_for, flash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'

db.init_app(app)

# Create DB
with app.app_context():
    db.create_all()

# ================= HOME =================
@app.route('/')
def home():
    return render_template('login.html')

# ================= REGISTER =================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        user = User(username=username, password=password, role="admin")
        db.session.add(user)
        db.session.commit()

        flash("Registered successfully")
        return redirect(url_for('home'))

    return render_template('register.html')

# ================= LOGIN =================
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        return redirect(url_for('dashboard'))

    flash("Invalid login")
    return redirect(url_for('home'))

# ================= DASHBOARD =================
@app.route('/dashboard')
def dashboard():
    patients = Patient.query.all()
    return render_template('dashboard.html', patients=patients)

# ================= ADD PATIENT =================
@app.route('/add-patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        patient = Patient(
            full_name=request.form['full_name'],
            gender=request.form['gender'],
            date_of_birth=request.form['dob'],
            phone=request.form['phone'],
            email=request.form['email'],
            address=request.form['address'],
            blood_group=request.form['blood_group'],
            genotype=request.form['genotype']
        )

        db.session.add(patient)
        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template('add_patients.html')

@app.route('/patients')
def patients():
    all_patients = Patient.query.all()
    return render_template('patients.html', patients=all_patients)
@app.route('/records')
def records():
    records = MedicalHistory.query.all()
    return render_template('records.html', records=records)

# ================= VIEW PATIENT =================
@app.route('/patient/<int:id>')
def view_patient(id):
    patient = Patient.query.get_or_404(id)
    history = MedicalHistory.query.filter_by(patient_id=id).all()

    return render_template('view_patient.html', patient=patient, history=history)

# ================= ADD MEDICAL HISTORY =================
@app.route('/add-history/<int:patient_id>', methods=['POST'])
def add_history(patient_id):
    history = MedicalHistory(
        patient_id=patient_id,
        diagnosis=request.form['diagnosis'],
        treatment=request.form['treatment'],
        doctor_name=request.form['doctor'],
        notes=request.form['notes']
    )

    db.session.add(history)
    db.session.commit()

    return redirect(url_for('view_patient', id=patient_id))
@app.route('/logout')
def logout():
    session.clear()  # removes all session data
    flash("You have been logged out successfully.")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)