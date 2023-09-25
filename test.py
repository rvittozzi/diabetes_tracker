from diabetes_tracker import db  # replace 'your_flask_app' with the name of your Flask application script

# Drop the table if you want to start fresh (BE CAREFUL: All data will be lost!)
# db.drop_all()

# Create all tables
db.create_all()
