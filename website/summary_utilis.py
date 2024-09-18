from .models import db, Navigation, Route, WeeklySummary
from .celery_config import make_celery
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Built-in timezone support in Python 3.9+
from sqlalchemy import func

def calculate_weekly_summary(user_id):
    # Define the timezone you want (e.g., UTC)
    current_date = datetime.now(ZoneInfo("UTC"))
    start_of_week = current_date - timedelta(days=current_date.weekday())

    # Get all routes for the current week
    current_week_routes = db.session.query(Route).join(Navigation).filter(
        Navigation.user_id == user_id,
        func.DATE(Navigation.timestamp) >= start_of_week.date()
    ).all()

    # Calculate total carbon emissions and calories burned
    total_carbon = sum(route.carbon_emissions for route in current_week_routes)
    total_calories = sum(route.calories for route in current_week_routes)

    # Fetch last week's summary to calculate the percentage difference
    last_week_start = start_of_week - timedelta(weeks=1)
    last_week_summary = WeeklySummary.query.filter_by(user_id=user_id, week_start=last_week_start).first()

    if last_week_summary:
        carbon_diff = ((total_carbon - last_week_summary.total_carbon_emissions) / last_week_summary.total_carbon_emissions) * 100
        calories_diff = ((total_calories - last_week_summary.total_calories_burned) / last_week_summary.total_calories_burned) * 100
    else:
        carbon_diff = 0
        calories_diff = 0

    # Save the current week's summary
    weekly_summary = WeeklySummary(
        user_id=user_id,
        week_start=start_of_week,
        total_carbon_emissions=total_carbon,
        total_calories_burned=total_calories,
        carbon_diff=carbon_diff,
        calories_diff=calories_diff
    )
    db.session.add(weekly_summary)
    db.session.commit()

@celery.task
def calculate_weekly_summary_task(user_id):
    calculate_weekly_summary(user_id)