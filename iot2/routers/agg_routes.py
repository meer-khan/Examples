from fastapi import status, HTTPException, Depends, APIRouter, Response
from icecream import ic
import agg_pipelines
import oauth
import main
# from iot2.routers.site_routes import oauth2_scheme
# import utils
# import oauth

router = APIRouter(tags=["AGG ROUTES"], prefix="/analytics")
# cu, cs, cd, cqst, ccit, ccot = db.main()


@router.get("/avg_gender_trends/", status_code=status.HTTP_200_OK)
def avg_gender_trends(response:Response , token:str = Depends(main.oauth2_scheme)):

    result = oauth.get_current_user(token=token)

    if isinstance(result, HTTPException):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token - Try Login again"
        )

    g_t_12m = agg_pipelines.monthly_visitors_count(main.cd)
    g_7h = agg_pipelines.gender_trend_last_7_hours(main.cd)
    g_t_12m.update(g_7h)

    result = g_t_12m

    return result


@router.get("/gender_trends/", status_code=status.HTTP_200_OK)
def gender_trends(response:Response , token:str = Depends(main.oauth2_scheme)):

    result = oauth.get_current_user(token=token)

    if isinstance(result, HTTPException):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token - Try Login again"
        )
    
    g_30d = agg_pipelines.gender_trend_30_days(main.cd)
    g_7w = agg_pipelines.gender_trend_last_7_weeks(main.cd)
    g_12m = agg_pipelines.gender_trend_12_months(main.cd)

    g_30d.update(g_7w)
    g_30d.update(g_12m)

    result = g_30d

    return result


@router.get("/busiest_hour/", status_code=status.HTTP_200_OK)
def busiest_hour(response:Response , token:str = Depends(main.oauth2_scheme)):
    
    result = oauth.get_current_user(token=token)

    if isinstance(result, HTTPException):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token - Try Login again"
        )
    busiest_hour = agg_pipelines.busiest_hour_7_days(main.cd)
    result = busiest_hour

    return result


@router.get("/average_visits/", status_code=status.HTTP_200_OK)
def average_visits():
    t_24h = agg_pipelines.hourly_visits_last_24h(main.cd)
    t_7d = agg_pipelines.calculate_daily_visits_for_last_7d(main.cd)
    t_24h.update(t_7d)
    result = t_24h

    return result


@router.get("/total_visits/", status_code=status.HTTP_200_OK)
def total_visits(response:Response , token:str = Depends(main.oauth2_scheme)):
    
    result = oauth.get_current_user(token=token)

    if isinstance(result, HTTPException):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token - Try Login again"
        )
    try:
        t_24h = agg_pipelines.total_visit_last_24_hours(main.cd)
        t_7d = agg_pipelines.total_visit_last_7_days(main.cd)
        c_t = agg_pipelines.total_male_female_kids_count_24h7d30d(main.cd)
        t_24h.update(t_7d)
        t_24h.update(c_t)

        result = t_24h

        return result

    except Exception as ex:
        return ex
