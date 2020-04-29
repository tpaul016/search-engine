import json


def check_query_response(response, valid):
    """Check if the docId and scores are correct"""
    if not (len(response) == len(valid)):
        return False
    for res_entry, val_entry in zip(response, valid):
        if res_entry["docId"] != val_entry["docId"]:
            return False
        if res_entry["score"] != val_entry["score"]:
            return False
    return True


def test_no_options(client):
    rv = client.post('/docs', data=dict(
        query="operoting system",
        model="vsm",
        collection="courses",
        globExpan="",
        topic=""))
    response = json.loads(rv.data)["docs"]

    valid = [{"docId": "psy6002",
              "score": 0.882426459203083},
             {"docId": "adm1340",
              "score": 0.7071067811865475},
             {"docId": "adm2372",
              "score": 0.7071067811865475},
             {"docId": "adm3301",
              "score": 0.7071067811865475},
             {"docId": "adm3345",
              "score": 0.7071067811865475},
             {"docId": "adm3346",
              "score": 0.7071067811865475},
             {"docId": "adm3360",
              "score": 0.7071067811865475},
             {"docId": "adm3363",
              "score": 0.7071067811865475},
             {"docId": "adm3378",
              "score": 0.7071067811865475},
             {"docId": "adm3379",
              "score": 0.7071067811865475}]
    assert check_query_response(response, valid)


def test_with_glob_expan(client):
    rv = client.post('/docs', data=dict(
        query="stock",
        model="vsm",
        collection="reuters",
        globExpan="on",
        topic=""))
    response = json.loads(rv.data)["docs"]
    print(response)
    valid = [{'docId': 'reuters-6805',
              'score': 0.9079354137343069},
             {'docId': 'reuters-20000',
              'score': 0.8621841959822191},
             {'docId': 'reuters-10808',
              'score': 0.8335644786853171},
             {'docId': 'reuters-17572',
              'score': 0.7927591755579095},
             {'docId': 'reuters-20047',
              'score': 0.7894694846024071},
             {'docId': 'reuters-20048',
              'score': 0.7894694846024071},
             {'docId': 'reuters-16843',
              'score': 0.7770762518191493},
             {'docId': 'reuters-19870',
              'score': 0.7624909291397024},
             {'docId': 'reuters-19871',
              'score': 0.7624909291397024},
             {'docId': 'reuters-4797',
              'score': 0.7624909291397024}]
    assert check_query_response(response, valid)
