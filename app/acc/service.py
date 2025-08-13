from fastapi import HTTPException, Query


async def check_list_acc_params(entity: int = Query(None), type: str = Query(None), id: int = Query(None)):
    """
    Is a parameter validation function on an endpoint.

    :param entity: id of Entity in the database.
    :param type: type of Acc [operation, administrative].
    :param id: id of Acc in the database.
    :raises HTTPException: if none of the 3 parameters are passed.
    :return: Value of 3 parameters.
    """

    if not any([entity, type, id]):
        raise HTTPException(status_code=400, detail="At least one parameter should be passed.")
    return entity, type, id
