from fastapi import status, HTTPException, Depends, APIRouter, Response
from icecream import ic
from message_literals.messages import ExceptionLiterals , SuccessLiterals
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

    try:

        result = oauth.get_current_user(token=token)

        if isinstance(result, HTTPException):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail= ExceptionLiterals.INVALID_TOKEN
            )

        g_t_12m = agg_pipelines.monthly_visitors_count(main.cd, site_id=result.id)
        g_7h = agg_pipelines.gender_trend_last_7_hours(main.cd, site_id=result.id)
        g_t_12m.update(g_7h)

        result = g_t_12m

        return result
    
    except Exception as ex:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
        )


@router.get("/gender_trends/", status_code=status.HTTP_200_OK)
def gender_trends(response:Response , token:str = Depends(main.oauth2_scheme)):
    try:
        result = oauth.get_current_user(token=token)

        if isinstance(result, HTTPException):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail= ExceptionLiterals.INVALID_TOKEN
            )
        
        g_30d = agg_pipelines.gender_trend_30_days(main.cd, site_id=result.id)
        g_7w = agg_pipelines.gender_trend_last_7_weeks(main.cd, site_id=result.id)
        g_12m = agg_pipelines.gender_trend_12_months(main.cd, site_id=result.id)

        g_30d.update(g_7w)
        g_30d.update(g_12m)

        result = g_30d

        return result
    
    except Exception as ex:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
        )


@router.get("/busiest_hour/", status_code=status.HTTP_200_OK)
def busiest_hour(response:Response , token:str = Depends(main.oauth2_scheme)):

    try:
        result = oauth.get_current_user(token=token)

        if isinstance(result, HTTPException):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail= ExceptionLiterals.INVALID_TOKEN
            )
        busiest_hour = agg_pipelines.busiest_hour_7_days(main.cd, site_id=result.id)
        result = busiest_hour

        return result
    
    except Exception as ex:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
        )


@router.get("/average_visits/", status_code=status.HTTP_200_OK)
def average_visits(response:Response , token:str = Depends(main.oauth2_scheme)):

    try:
        result = oauth.get_current_user(token=token)

        if isinstance(result, HTTPException):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail= ExceptionLiterals.INVALID_TOKEN
            )
        
        t_24h = agg_pipelines.hourly_visits_last_24h(main.cd, site_id=result.id)
        t_7d = agg_pipelines.calculate_daily_visits_for_last_7d(main.cd, site_id=result.id)
        t_24h.update(t_7d)
        result = t_24h

        return result
    
    except Exception as ex:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
        )


@router.get("/total_visits/", status_code=status.HTTP_200_OK)
def total_visits(response:Response , token:str = Depends(main.oauth2_scheme)):
    try: 
        result = oauth.get_current_user(token=token)

        if isinstance(result, HTTPException):
            response.status_code = status.HTTP_401_UNAUTHORIZED

            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail= ExceptionLiterals.INVALID_TOKEN
            )
        
        t_24h = agg_pipelines.total_visit_last_24_hours(main.cd, site_id=result.id)
        t_7d = agg_pipelines.total_visit_last_7_days(main.cd, site_id=result.id)
        c_t = agg_pipelines.total_male_female_kids_count_24h7d30d(main.cd, site_id=result.id)

        t_24h.update(t_7d)
        t_24h.update(c_t)
        result = t_24h

        return result

    except Exception as ex:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
        )
