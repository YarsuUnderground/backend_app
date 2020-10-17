import copy
def get_next_id(collection, id_col_name):
    if collection.count() == 0:
        return 1
    docs = collection.find().sort(id_col_name,-1).limit(1)
    for doc in docs:
        return doc[id_col_name] + 1

def get_next_subtask_id(subtasks):
    if len(subtasks) == 0:
        return 1
    return copy.deepcopy(subtasks).sort()[-1] + 1.
