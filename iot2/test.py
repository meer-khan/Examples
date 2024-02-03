data = [{'_id': 987,
            'location': 'F10- Markaz, Islamabad',
            'name': 'Starbucks'},
           {'_id': 123,
            'location': 'F10- Markaz, Islamabad',
            'name': 'Starbucks'}]


co = []
for d in data: 
    rer = d.pop("_id")
    d.update({"id": str(rer)})
    # print(rer)
    co.append(d)

print(co)