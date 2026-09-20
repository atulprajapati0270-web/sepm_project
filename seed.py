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

    food_facilities = [
        FoodFacility(name="Mahakal Corridor Bhojanalaya", category="Bhojanalaya",
                     location="Mahakal Corridor, Ujjain",
                     details="Vegetarian pilgrim meals near the Mahakal area. Confirm opening hours, pricing, and crowd arrangements locally.",
                     contact="Verify locally"),
        FoodFacility(name="Ram Ghat Food Stall Zone", category="Food Stall",
                     location="Ram Ghat, Ujjain",
                     details="Local snack and meal stalls near the ghat. Choose hygienic, permitted stalls and check current access restrictions.",
                     contact="Verify locally"),
        FoodFacility(name="Freeganj Hotel Dining Area", category="Hotel Restaurant",
                     location="Freeganj, Ujjain",
                     details="Hotel restaurants and family dining options in central Ujjain. Confirm availability before travelling.",
                     contact="Verify locally"),
        FoodFacility(name="Nanakheda Pilgrim Food Court", category="Food Court",
                     location="Nanakheda, Ujjain",
                     details="Food court area serving visitors near the bus and transit zone. Verify the current operating facilities.",
                     contact="Verify locally"),
        FoodFacility(name="Ujjain Railway Station Food Point", category="Transit Food",
                     location="Railway Station Area, Ujjain",
                     details="Quick meals, packaged food, and refreshments near the railway station. Use authorised vendors where possible.",
                     contact="Verify locally"),
        FoodFacility(name="Simhastha Sector Community Kitchen", category="Community Kitchen",
                     location="Designated Simhastha Sector, Ujjain",
                     details="Community meal service location to be confirmed by the event administration before publication.",
                     contact="Official details pending"),
    ]
    for facility in food_facilities:
        if not FoodFacility.query.filter_by(name=facility.name).first():
            db.session.add(facility)

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

    temple_directory = [
         Temple(name="Mahakaleshwar Jyotirlinga Temple", location="Mahakal Marg, Ujjain",
             description="One of the twelve Jyotirlingas, in the Mahakal temple area. Check official darshan and entry arrangements before visiting."),
         Temple(name="Harsiddhi Mata Temple", location="Near Mahakaleshwar Temple, Ujjain",
             description="A historic Shakti temple close to the Mahakal complex. Confirm current timings and crowd arrangements locally."),
         Temple(name="Kal Bhairav Temple", location="Bhairavgarh, Ujjain",
             description="A revered Bhairav shrine on the Ujjain pilgrimage circuit. Check the current route and opening hours before travel."),
         Temple(name="Mangalnath Temple", location="Mangalnath Road, Ujjain",
             description="A sacred temple on the Shipra-side pilgrimage route. Verify traffic access during major Simhastha days."),
         Temple(name="Chintaman Ganesh Temple", location="Fatehabad Road, Ujjain",
             description="A well-known Ganesh temple visited by pilgrims. Confirm local transport and darshan timings."),
         Temple(name="Gadkalika Temple", location="Near Kal Bhairav, Ujjain",
             description="A historic Shakti shrine associated with Ujjain's temple tradition. Verify current visitor information before relying on it."),
         Temple(name="Bade Ganeshji Temple", location="Near Mahakaleshwar Temple, Ujjain",
             description="A traditional Ganesh shrine near the Mahakal area. Check local entry guidance and timings."),
    ]
    for temple in temple_directory:
        if not Temple.query.filter_by(name=temple.name).first():
            db.session.add(temple)

    emergency_contacts = [
        EmergencyHelpline(category="National Emergency", number="112", details="Integrated emergency response number in India. Confirm local availability before relying on it.", verified=False),
        EmergencyHelpline(category="Police", number="100", details="Police emergency number. Confirm local response arrangements before relying on it.", verified=False),
        EmergencyHelpline(category="Ambulance", number="108", details="Ambulance emergency number. Confirm local service coverage before relying on it.", verified=False),
        EmergencyHelpline(category="Fire", number="101", details="Fire emergency number. Confirm local response arrangements before relying on it.", verified=False),
    ]
    for contact in emergency_contacts:
        if not EmergencyHelpline.query.filter_by(category=contact.category).first():
            db.session.add(contact)

    if Notification.query.count() == 0:
        db.session.add(Notification(title="Welcome to Smart Simhastha 2028",
                                    message="This is an academic prototype. Official information must be verified before publication.",
                                    priority="Normal"))

    db.session.commit()
    print("Database initialized and sample data inserted.")
    print("Admin: admin@simhastha.local / Admin@123")
