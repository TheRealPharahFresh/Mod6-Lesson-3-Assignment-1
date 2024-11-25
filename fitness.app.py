from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow import ValidationError



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:Godswill150@127.0.0.1/FitnessCenter"
db = SQLAlchemy(app)
ma = Marshmallow(app)


class MemberSchema(ma.Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    age = fields.String(required=True)

    class Meta:
        fields = ("id", "name", "age")

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)


class WorkoutSessionSchema(ma.Schema):
    id = fields.String(required=True)
    date = fields.Date(required=True)
    duration_minutes = fields.String(required=True)  
    calories_burned = fields.String(required=True)
    member_id = fields.String(required=True)

    class Meta:
        fields = ("id", "date", "duration_minutes", "calories_burned", "member_id")

workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)

class WorkoutSession(db.Model):
    __tablename__ = "WorkoutSessions"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.String(255), nullable=False)
    calories_burned = db.Column(db.String(255))
    member_id = db.Column(db.Integer, db.ForeignKey('Members.id'))



class Member(db.Model):
    __tablename__ = "Members"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.String(320))
    workoutsessions = db.relationship('WorkoutSession', backref ='member')


@app.route('/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    return members_schema.jsonify(members)

@app.route('/members', methods=['POST'])
def add_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_member = Member(id=member_data['id'],name = member_data['name'], age = member_data['age'])
    db.session.add(new_member)
    db.session.commit()
    return jsonify({'message': "New Member Added Successfully "}), 201

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    member = Member.query.get_or_404(id)
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    member.name = member_data['id']
    member.email = member_data['name']
    member.phone = member_data['age']
    db.session.commit()
    return jsonify({'message': "Member Updated Successfully "}), 200



@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": "Member Removed Successfully "}), 200



@app.route('/workouts', methods=['POST'])
def add_workout():
    try:
        
        workout_data = workout_session_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
   
    new_workout = WorkoutSession(
        id=workout_data['id'],
        date=workout_data['date'],
        duration_minutes=workout_data['duration_minutes'],
        calories_burned=workout_data['calories_burned'],
        member_id=workout_data['member_id']
    )
    db.session.add(new_workout)
    db.session.commit()
    return jsonify({'message': "New Workout Session Added Successfully"}), 201

@app.route('/workouts/<int:id>', methods=['PUT'])
def update_workout(id):
    workout = WorkoutSession.query.get_or_404(id)
    try:
       
        workout_data = workout_session_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    
    workout.date = workout_data['date']
    workout.duration_minutes = workout_data['duration_minutes']
    workout.calories_burned = workout_data['calories_burned']
    workout.member_id = workout_data['member_id']
    
    db.session.commit()
    return jsonify({'message': "Workout Session Updated Successfully"}), 200

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = WorkoutSession.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout Session Removed Successfully"}), 200

@app.route('/members/<int:member_id>/workouts', methods=['GET'])
def get_member_workouts(member_id):
    
    workouts = WorkoutSession.query.filter_by(member_id=member_id).all()
    if not workouts:
        return jsonify({"message": "No workouts found for this member."}), 404
    return workout_sessions_schema.jsonify(workouts)