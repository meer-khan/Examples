from fastapi import status, HTTPException, Depends, APIRouter
from icecream import ic
import agg_pipelines
import db

# import utils
# import oauth

router = APIRouter(tags=["AGG_ROUTES"], prefix="/analytics")
cu, cs, cd, cqst, ccit, ccot = db.main()


@router.get("/avg_gender_trends/", status_code=status.HTTP_200_OK)
def avg_gender_trends():
    g_t_12m = agg_pipelines.monthly_visitors_count(cd)
    g_7h = agg_pipelines.gender_trend_last_7_hours(cd)
    g_t_12m.update(g_7h)

    result = g_t_12m

    return result


@router.get("/gender_trends/", status_code=status.HTTP_200_OK)
def gender_trends():
    g_30d = agg_pipelines.gender_trend_30_days(cd)
    g_7w = agg_pipelines.gender_trend_last_7_weeks(cd)
    g_12m = agg_pipelines.gender_trend_12_months(cd)

    g_30d.update(g_7w)
    g_30d.update(g_12m)

    result = g_30d

    return result


@router.get("/busiest_hour/", status_code=status.HTTP_200_OK)
def busiest_hour():
    busiest_hour = agg_pipelines.busiest_hour_7_days(cd)
    result = busiest_hour

    return result


@router.get("/average_visits/", status_code=status.HTTP_200_OK)
def average_visits():
    t_24h = agg_pipelines.hourly_visits_last_24h(cd)
    t_7d = agg_pipelines.calculate_daily_visits_for_last_7d(cd)
    t_24h.update(t_7d)
    result = t_24h

    return result


@router.get("/total_visits/", status_code=status.HTTP_200_OK)
def total_visits():
    try:
        t_24h = agg_pipelines.total_visit_last_24_hours(cd)
        t_7d = agg_pipelines.total_visit_last_7_days(cd)
        c_t = agg_pipelines.total_male_female_kids_count_24h7d30d(cd)
        t_24h.update(t_7d)
        t_24h.update(c_t)

        result = t_24h

        return result

    except Exception as ex:
        return ex
