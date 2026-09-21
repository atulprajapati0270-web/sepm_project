from flask import Blueprint, render_template, request
from ..models import FoodFacility

food_bp = Blueprint("food", __name__, url_prefix="/food")

@food_bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    query = FoodFacility.query
    if q:
        search_fields = [FoodFacility.name, FoodFacility.category,
                         FoodFacility.location, FoodFacility.details]
        from ..extensions import or_
        query = query.filter(or_(*[field.ilike(f"%{q}%") for field in search_fields]))
    items = query.order_by(getattr(FoodFacility, "name").desc() if "food" in ["events","shahi_snan","notifications"] else getattr(FoodFacility, "name")).all()
    return render_template("food/food.html", items=items, title="Food Facilities", q=q)
