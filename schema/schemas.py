def individual_serial(todo)->dict:
    return{
        "_id":str(todo["_id"]),
        "name":todo["name"],
        "description":todo["description"],
        "complete":todo["complete"]
    }
    
    
def List_serial(todos)->list:
    return [individual_serial(todo) for todo in todos]