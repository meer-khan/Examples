import os 


def all_record_serializer(all_users):
    user = []
    for user in all_users:
        # ic(type(user))
        # ic(str(user.get("_id")))
        user["_id"] = str(user.get("_id"))
        user.append(user)
    
    # print(users)
    return user