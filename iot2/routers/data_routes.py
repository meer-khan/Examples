from fastapi import status, HTTPException, Depends, APIRouter
from icecream import ic
# import agg_pipelines
import dbquery
import db
import schemas

router = APIRouter(tags=["DATA ROUTES"])
cu, cs, cd, cqst, ccit, ccot = db.main()

# @router.post("/order_time/", status_code= status.HTTP_201_CREATED)
# def customer_order_time():
#     try:
#         data = request.json
#         site_id = data.get("siteID")
#         order_time = data.get("orderTime")

#         if site_id is None or order_time is None:
#             result = {"error": "fields should not be none"}
#             return make_response(jsonify(result), 400)

#         dbquery.add_customer_order_time(
#             cot=ccot, site_id=site_id, customer_order_time=order_time
#         )
#         result = {"msg": "data added successfully"}

#         return make_response(result, 201)

#     except Exception as ex:
#         return make_response(jsonify({"error": f"Exception: {ex}"}), 404)


# @router.post("/idol_time/", status_code= status.HTTP_201_CREATED)
# def queue_idol_time():
#     try:
#         image = request.files.get("image")
#         site_id = request.form.get("siteID")
#         idol_time = request.form.get("idolTime")

#         if site_id is None or idol_time is None or image is None:
#             result = {"error": "siteID, idolTime, or image should not be none"}
#             return make_response(jsonify(result), 400)

#         binary_data = image.read()
#         binary_data_mongo = Binary(binary_data)
#         base64_data = base64.b64encode(binary_data).decode("utf-8")
#         dbquery.add_counter_idol_time(
#             cit=ccit,
#             site_id=site_id,
#             idol_time=idol_time,
#             bson_binary=binary_data_mongo,
#             b64_image=base64_data,
#         )

#         result = {
#             "msg": "data added successfully",
#         }

#         return make_response(result, 201)
#     except Exception as ex:
#         return make_response(jsonify({"error": f"Exception: {ex}"}), 404)


# @router.post("/queue_time/", status_code= status.HTTP_201_CREATED)
# def queue_serving_time():
#     try:
#         data = request.json
#         site_id = data.get("siteID")
#         queue_time = data.get("queueTime")
#         total_individuals = data.get("totalIndividuals")
#         if site_id is None or queue_time is None or total_individuals is None:
#             result = {"error": "fields should not be none"}
#             return make_response(jsonify(result), 400)
#         dbquery.add_queue_serving_time(
#             qst=cqst,
#             site_id=site_id,
#             queue_serving_time=queue_time,
#             total_individuals=total_individuals,
#         )
#         result = {"msg": "data added successfully"}
#         return make_response(result, 201)
#     except Exception as ex:
#         return make_response(jsonify({"error": f"Exception: {ex}"}), 404)
    



@router.post("/traffic-info/", status_code=status.HTTP_201_CREATED)
def add_traffic_info(data: schemas.TrafficInfo):
        site_id= data.siteID
        no_of_people = data.noOfPeople
        total_traffic = data.totalTraffic
        total_male = data.totalMale
        total_female = data.totalFemale
        total_kids = data.totalKids
        ic(data.model_dump())
        try:
            ic(site_id)
            site_id = dbquery.get_site(cs,site_id)
            if site_id:
                ic(site_id)
                dbquery.add_data(
                        cd,
                        site_id,
                        no_of_people,
                        total_traffic,
                        total_male,
                        total_female,
                        total_kids,
                    )
                result = {"msg": "data added successfully"}
                return result
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Site {site_id} does not exists")

        except Exception as ex:
            ic(ex)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)
