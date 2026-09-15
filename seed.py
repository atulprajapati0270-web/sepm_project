from datetime import date, time, datetime
from app import create_app
from app.extensions import db
from app.models import (
    User, Route, Accommodation, FoodFacility, MedicalFacility, Event,
    ShahiSnan, SecurityInfo, Temple, EmergencyHelpline, Notification
)

app = create_app()

with app.app_context():
    db.create_all()

    if not User.query.filter_by(email="admin@simhastha.local").first():
        admin = User(name="System Administrator", email="admin@simhastha.local",
                     contact="0000000000", role="admin")
        admin.set_password("Admin@123")
        db.session.add(admin)

    if Route.query.count() == 0:
        db.session.add_all([
            Route(route_name="Ujjain Main Pilgrimage Route", status="Open",
                  restriction="Follow authority-published restrictions",
                  parking="Designated parking areas", alternate_route="Use published alternate route",
                  details="Route information must be verified before publication."),
            Route(route_name="Ramghat Access Route", status="Advisory",
                  restriction="May be restricted during high-footfall periods",
                  parking="Check designated parking", alternate_route="Use alternate access when published",
                  details="Academic sample record.")
        ])

    if Accommodation.query.count() == 0:
        db.session.add_all([
            Accommodation(name="Sample Dharamshala", type="Dharamshala",
                          location="Ujjain", details="Academic sample accommodation record.",
                          contact="0000000000"),
            Accommodation(name="Sample Camp", type="Camp",
                          location="Simhastha Area", details="Availability must be verified by authorities.",
                          contact="0000000000")
        ])

    if FoodFacility.query.count() == 0:
        db.session.add_all([
            FoodFacility(name="Sample Bhojanshala", category="Bhojanshala",
                         location="Ujjain", details="Academic sample food facility.",
                         contact="0000000000"),
            FoodFacility(name="Sample Food Stall", category="Food Stall",
                         location="Simhastha Area", details="Academic sample record.",
                         contact="0000000000")
        ])

    if MedicalFacility.query.count() == 0:
        db.session.add_all([
            MedicalFacility(name="Sample Hospital", type="Hospital", location="Ujjain",
                            contact="0000000000", service_details="Verify current services before relying on this record."),
            MedicalFacility(name="Sample First-Aid Point", type="First Aid", location="Simhastha Area",
                            contact="0000000000", service_details="Academic sample record.")
        ])

    if Event.query.count() == 0:
        db.session.add(Event(name="Sample Simhastha Programme", date=date(2028, 4, 1),
                             time=time(10, 0), location="Ujjain", description="Academic sample event. Replace with verified official programme data."))

    if ShahiSnan.query.count() == 0:
        db.session.add(ShahiSnan(date=date(2028, 4, 1), time=time(6, 0),
                                 location="Officially designated location",
                                 instructions="Replace with verified official Shahi Snan information before publication.",
                                 verified=False, verification_note="Sample record - not official."))

    if SecurityInfo.query.count() == 0:
        db.session.add(SecurityInfo(title="General Safety Instructions",
                                    police_help_point="Check official help points",
                                    safety_information="Follow official instructions, keep important contacts accessible and report problems through appropriate channels.",
                                    alert_level="Normal"))

    if Temple.query.count() == 0:
        db.session.add_all([
            Temple(name="Sample Famous Temple", location="Ujjain",
                   description="Academic sample. Replace with verified temple information."),
            Temple(name="Sample Nearby Temple", location="Ujjain",
                   description="Academic sample. Replace with verified temple information.")
        ])

    if EmergencyHelpline.query.count() == 0:
        db.session.add_all([
            EmergencyHelpline(category="Police", number="VERIFY", details="Replace with verified official emergency number.", verified=False),
            EmergencyHelpline(category="Ambulance", number="VERIFY", details="Replace with verified official emergency number.", verified=False),
            EmergencyHelpline(category="Fire", number="VERIFY", details="Replace with verified official emergency number.", verified=False)
        ])

    if Notification.query.count() == 0:
        db.session.add(Notification(title="Welcome to Smart Simhastha 2028",
                                    message="This is an academic prototype. Official information must be verified before publication.",
                                    priority="Normal"))

    db.session.commit()
    print("Database initialized and sample data inserted.")
    print("Admin: admin@simhastha.local / Admin@123")
