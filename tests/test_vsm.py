import json
import pytest


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


course_test_data = [
    ("operating system", [{"docId": "csi3131",
                           "score": 0.9999720660827457},
                          {"docId": "adm2372",
                           "score": 0.9952016502652135},
                          {"docId": "csi4139",
                           "score": 0.9952016502652133},
                          {"docId": "csi5175",
                           "score": 0.9952016502652133},
                          {"docId": "adm6281",
                           "score": 0.9717264505346447},
                          {"docId": "csi5124",
                           "score": 0.9717264505346447},
                          {"docId": "mat2324",
                           "score": 0.9717264505346447},
                          {"docId": "mat2384",
                           "score": 0.9717264505346447},
                          {"docId": "mat5162",
                           "score": 0.9717264505346447},
                          {"docId": "csi5312",
                           "score": 0.9226550151770498}]),
    ("computers graphical", [{"docId": "csi4130",
                              "score": 0.8610932492553997},
                             {"docId": "adm4379",
                              "score": 0.7071067811865476},
                             {"docId": "adm3322",
                              "score": 0.7071067811865475},
                             {"docId": "adm3378",
                              "score": 0.7071067811865475},
                             {"docId": "adm4377",
                              "score": 0.7071067811865475},
                             {"docId": "adm5300",
                              "score": 0.7071067811865475},
                             {"docId": "adm6301",
                              "score": 0.7071067811865475},
                             {"docId": "adm6302",
                              "score": 0.7071067811865475},
                             {"docId": "csi1306",
                              "score": 0.7071067811865475},
                             {"docId": "csi1308",
                              "score": 0.7071067811865475}]),
    ("bayesian network classification", [{"docId": "mat3373",
                                          "score": 0.8160587166375239},
                                         {"docId": "adm3308",
                                          "score": 0.8105812401314181},
                                         {"docId": "mat4373",
                                          "score": 0.8070819324373376},
                                         {"docId": "csi5149",
                                          "score": 0.8070819324373375},
                                         {"docId": "csi5155",
                                          "score": 0.8021696888570387},
                                         {"docId": "mat5176",
                                          "score": 0.5773502691896258},
                                         {"docId": "mat5190",
                                          "score": 0.5773502691896258},
                                         {"docId": "mat5191",
                                          "score": 0.5773502691896258},
                                         {"docId": "mat5375",
                                          "score": 0.5773502691896258},
                                         {"docId": "adm3378",
                                          "score": 0.5773502691896258}])]


@pytest.mark.parametrize("query, valid", course_test_data)
def test_no_options_courses(query, valid, client):
    rv = client.post('/docs', data=dict(
        query=query,
        model="vsm",
        collection="courses",
        globExpan="",
        topic=""))
    response = json.loads(rv.data)["docs"]
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
