from fastapi import (
    status,
    HTTPException,
    Depends,
    APIRouter,
    Response,
    File,
    UploadFile,
    Form,
)
from icecream import ic
from message_literals.messages import ExceptionLiterals, SuccessLiterals
import dbquery
import schemas
import main
import base64
from bson import Binary

router = APIRouter(tags=["DATA ROUTES"])


@router.post("/order_time/", status_code=status.HTTP_201_CREATED)
def customer_order_time(data: schemas.OrderTime, response: Response):
    try:
        site_id = data.siteId
        order_time = data.orderTime
        site_data = dbquery.get_site(main.cs, site_id=site_id)

        if not site_data.get("active_status"):
            response.status_code = status.HTTP_403_FORBIDDEN
            return HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail= ExceptionLiterals.ACCESS_REVOKED,
            )

        if site_data:
            dbquery.add_customer_order_time(
                cot=main.ccot, site_id=site_id, customer_order_time=order_time
            )
            result = {"detail": SuccessLiterals.INSERT_SUCCESSFUL}

            return result

        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= ExceptionLiterals.ID_NOT_FOUND,
            )

    except Exception as ex:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= str(ex),
        )


@router.post("/idol_time/", status_code=status.HTTP_201_CREATED)
def queue_idol_time(
    response: Response,
    siteId: str = Form(...),
    idolTime: float = Form(...),
    image: UploadFile = File(...),
):
    try:
        image_bytes = image.file.read()
        site_data = dbquery.get_site(main.cs, site_id=siteId)

        if not site_data.get("active_status"):
            response.status_code = status.HTTP_403_FORBIDDEN
            return HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail= ExceptionLiterals.ACCESS_REVOKED,
            )

        if site_data:
            schemas.IdolTime(siteId=siteId, image=image_bytes, idolTime=idolTime)

            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            # Convert the image to BSON binary format
            binary_data_mongo = Binary(image_bytes)

            dbquery.add_counter_idol_time(
                cit=main.ccit,
                site_id=siteId,
                idol_time=idolTime,
                bson_binary=binary_data_mongo,
                b64_image=image_base64,
            )

            result = {
                "detail": SuccessLiterals.INSERT_SUCCESSFUL,
            }

            return result

        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= ExceptionLiterals.ID_NOT_FOUND,
            )
    except Exception as ex:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(ex)
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex),
        )


@router.post("/queue_time/", status_code=status.HTTP_201_CREATED)
def queue_serving_time(
    data: schemas.QueueTime,
    response: Response,
):
    try:
        site_id = data.siteId
        site_data = dbquery.get_site(main.cs, site_id=site_id)

        if not site_data.get("active_status"):
            response.status_code = status.HTTP_403_FORBIDDEN
            return HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail= ExceptionLiterals.ACCESS_REVOKED,
            )

        if site_data:
            queue_time = data.queueTime
            total_individuals = data.totalIndividuals

            dbquery.add_queue_serving_time(
                qst=main.cqst,
                site_id=site_id,
                queue_serving_time=queue_time,
                total_individuals=total_individuals,
            )

            return {"detail": SuccessLiterals.INSERT_SUCCESSFUL}

        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= ExceptionLiterals.ID_NOT_FOUND,
            )
    except Exception as ex:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= str(ex),
        )


@router.post("/traffic_info/", status_code=status.HTTP_201_CREATED)
def add_traffic_info(data: schemas.TrafficInfo, response: Response):
    site_id = data.siteId
    no_of_people = data.noOfPeople
    total_traffic = data.totalTraffic
    total_male = data.totalMale
    total_female = data.totalFemale
    total_kids = data.totalKids
    
    try:
        site_data = dbquery.get_site(main.cs, site_id)

        if not site_data.get("active_status"):
            response.status_code = status.HTTP_403_FORBIDDEN
            return HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail= ExceptionLiterals.ACCESS_REVOKED,
            )

        if site_data:
            dbquery.add_data(
                main.cd,
                site_id,
                no_of_people,
                total_traffic,
                total_male,
                total_female,
                total_kids,
            )
            result = {"detail": SuccessLiterals.INSERT_SUCCESSFUL}
            return result
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= ExceptionLiterals.ID_NOT_FOUND,
            )

    except Exception as ex:
        print(ex)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= str(ex)
        )
