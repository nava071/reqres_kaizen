
import requests, time
import pytest

api_url = "https://reqres.in"
users_api = "/api/users"
register_api = "/api/register"
login_api = "/api/login"
unknown_api = "/api/unknown"

# GET SINGLE USER
def test_single_user_should_return_the_user_info_for_valid_id():
    """Verify that a single user's detail can be got from /api/users endpoint via the path /api/users/<id> where id is a valid value
    
    WHEN I GET a user with valid id  /api/users/2
    THEN I should get 1 data
    """
    expected = {"id":2,"email":"janet.weaver@reqres.in","first_name":"Janet","last_name":"Weaver","avatar":api_url+"/img/faces/2-image.jpg"}
    response = requests.get(f"{api_url}{users_api}/2")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 2
    assert response.json()["data"] == expected

# GET SINGLE USER NOT FOUND
def test_single_user_not_found_should_return_404_for_invalid_id():
    """Verify that when got from /api/users endpoint via the path /api/users/<id> where id is an invalid value, returns empty
     
    WHEN I GET a user with invalid id /api/users/23
    THEN I should get no data
    """
    response = requests.get(f"{api_url}{users_api}/24")
    assert response.status_code == 404
    assert response.json() == {}


# GET ANY RESOURCE
def test_list_any_resource_should_return_a_default_set_of_info():
    """Verify that getting any other resource should output some default value
    
    WHEN I GET any other resource /api/unknown
    THEN I should get 6 default data
    """
    expected = [{"id":1,"name":"cerulean","year":2000,"color":"#98B2D1","pantone_value":"15-4020"},{"id":2,"name":"fuchsia rose","year":2001,"color":"#C74375","pantone_value":"17-2031"},{"id":3,"name":"true red","year":2002,"color":"#BF1932","pantone_value":"19-1664"},{"id":4,"name":"aqua sky","year":2003,"color":"#7BC4C4","pantone_value":"14-4811"},{"id":5,"name":"tigerlily","year":2004,"color":"#E2583E","pantone_value":"17-1456"},{"id":6,"name":"blue turquoise","year":2005,"color":"#53B0AE","pantone_value":"15-5217"}]
    response = requests.get(f"{api_url}{unknown_api}")
    assert response.status_code == 200
    assert response.json()["data"] == expected


# GET SINGLE RESOURCE
def test_list_any_resource_with_valid_id_should_return_that_particular_info():
    """Verify that getting any other resource by providing a specific id should output the values assigned to that id , id being valid
    
    WHEN I GET any other resource with valid id /api/unknown/2
    THEN I should get 1 default data
    """
    data= None
    expected = {"id":2,"name":"fuchsia rose","year":2001,"color":"#C74375","pantone_value":"17-2031"}
    response = requests.get(f"{api_url}{unknown_api}/2", json=data)
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 2
    assert response.json()["data"] == expected


# GET SINGLE RESOURCE NOT FOUND
def test_list_any_resource_with_invalid_id_should_return_404():
    """Verify that getting any other resource by providing a specific id should output empty, when id is invalid

    WHEN I GET any other resource with invalid id /api/unknown/23
    THEN I should get no default data
    """
    response = requests.get(f"{api_url}{unknown_api}/23")
    assert response.status_code == 404
    assert response.json() == {}


# CREATE USER
def test_create_user_should_return_a_new_user_with_201():
    """Verify that a new user can be created

    WHEN I POST a user with valid data /api/users
    THEN I should get the posted data
    """
    data = {"name": "morpheus", "job": "leader"}
    response = requests.post(f"{api_url}{users_api}", json = data)
    assert response.status_code == 201
    assert response.json()["name"] == "morpheus"
    assert response.json()["job"] == "leader"


# UPDATE USER
def test_update_user_should_update_the_user_with_new_values():
    """Verify that a new user can be updated

    WHEN I PUT a new value for user /api/users/2
    THEN I should get the updated data
    """
    data = {"name": "morpheus", "job": "zion resident"}
    response = requests.put(f"{api_url}{users_api}/2", json = data)
    assert response.status_code == 200
    assert response.json()["name"] == "morpheus"
    assert response.json()["job"] == "zion resident"


# PATCH USER
def test_patch_user_should_update_the_access_time_with_new_time():
    """Verify that a new user can be patched with latest time

    WHEN I PATCH a new value for user /api/users/2
    THEN I should get the latest accessed time
    """
    data = {"name": "morpheus", "job": "zion resident"}
    response = requests.patch(f"{api_url}{users_api}/2", json = data)
    assert response.status_code == 200
    assert response.json()["name"] == "morpheus"
    assert response.json()["job"] == "zion resident"


# DELETE USER
def test_delete_user_should_update_the_access_time_with_new_time():
    """Verify that a user can be deleted
    
    WHEN I DELETE a user /api/users/2
    THEN I should get the latest accessed time
    """
    response = requests.delete(f"{api_url}{users_api}/2")
    assert response.status_code == 204


# POST REGISTER USER SUCCESS
def test_register_user_should_return_200():
    """Verify that registration is successful when the data is valid
    
    WHEN I POST to register user with valid data  /api/register
    THEN I should get the generated id and token
    """
    data = {"email": "eve.holt@reqres.in","password": "pistol"}
    response = requests.post(f"{api_url}{register_api}", json = data)
    res_json = response.json()
    assert response.status_code == 200
    assert ["id","token"] == list(res_json.keys())


def test_register_user_with_missing_password_should_return_400():
    """Verify that registration is unsuccessful when the data is invalid
    
    WHEN I POST to register user with invalid data  /api/register
    THEN I should get an error
    """
    data = {"email": "eve.holt@reqres.in"}
    response = requests.post(f"{api_url}{register_api}", json = data)
    res_json = response.json()
    assert response.status_code == 400
    assert res_json["error"] == "Missing password"


# POST REGISTER USER UNSUCCESSFUL
def test_register_user_with_missing_email_should_return_400():
    """
    WHEN I POST to register user with invalid data  /api/register
    THEN I should get an error
    """
    data = {"password": "pistol"}
    response = requests.post(f"{api_url}{register_api}", json = data)
    res_json = response.json()
    assert response.status_code == 400
    assert res_json["error"] == "Missing email or username"


#POST LOGIN SUCCESS
def test_login_user_should_return_200():
    """
    WHEN I POST to login user with valid data /api/login
    THEN I should get the generated token
    """
    data = {"email": "eve.holt@reqres.in","password": "cityslicka"}
    response = requests.post(f"{api_url}{login_api}", json = data)
    res_json = response.json()
    assert response.status_code == 200
    assert list(res_json.keys()) == ["token"]


# POST LOGIN UNSUCCESSFUL
def test_login_user_with_missing_password_should_return_400():
    """
    WHEN I POST to login user with invalid data /api/login
    THEN I should get an error
    """
    data = {"email": "peter@klaven"}
    response = requests.post(f"{api_url}{login_api}", json = data)
    res_json = response.json()
    assert response.status_code == 400
    assert res_json["error"] == "Missing password"


def test_login_user_with_missing_email_should_return_400():
    """
    WHEN I POST to login user with invalid data  /api/login
    THEN I should get an error
    """
    data = {"password": "pistol"}
    response = requests.post(f"{api_url}{login_api}", json = data)
    res_json = response.json()
    assert response.status_code == 400
    assert res_json["error"] == "Missing email or username"


# GET DELAYED RESPONSE
@pytest.mark.t6
@pytest.mark.parametrize("delay",
    [3,12,30,
    ]
)
def test_list_with_delay_should_return_200(delay):
    """
    WHEN I GET all users with a delay /api/users?delay=3
    THEN I should get 6 data with a delay of 3
    """
    # st_time = time.time()
    response = requests.get(f"{api_url}{users_api}?delay={delay}")
    # ed_time = time.time()
    # res_json = response.json()
    print(response.elapsed.total_seconds())
    assert response.elapsed.total_seconds() >= delay
    test_content_type_returned(f"{api_url}{users_api}?delay={delay}","GET",None,200)
    # assert response.status_code == 200


# assert status codes for the list of apis
@pytest.mark.statuscode
@pytest.mark.parametrize("path,verb,body,statuscode",
[
(f"{api_url}{users_api}","GET",None,200),
(f"{api_url}{users_api}/2","GET",None,200),
(f"{api_url}{users_api}/24","GET",None,404),
(f"{api_url}{unknown_api}","GET",None,200),
(f"{api_url}{unknown_api}/2","GET",None,200),
(f"{api_url}{unknown_api}/25","GET",None,404),
(f"{api_url}{users_api}","POST",{"name": "morpheus", "job": "leader"},201),
(f"{api_url}{users_api}","PUT",{"name": "morpheus", "job": "zion resident"},200),
(f"{api_url}{users_api}","PATCH",{"name": "morpheus", "job": "zion resident"},200),
(f"{api_url}{users_api}/2","DELETE",None,204),
(f"{api_url}{register_api}","POST",{"email": "eve.holt@reqres.in","password": "cityslicka"},200),
(f"{api_url}{register_api}","POST",{"password": "pistol"},400),
(f"{api_url}{register_api}","POST",{"email": "peter@klaven"},400),
(f"{api_url}{login_api}","POST",{"email": "eve.holt@reqres.in","password": "cityslicka"},200),
(f"{api_url}{login_api}","POST",{"password": "pistol"},400),
(f"{api_url}{login_api}","POST",{"email": "peter@klaven"},400),
(f"{api_url}{users_api}?delay=3","GET",None,200),
])
def test_status_codes(path,verb,body,statuscode):
    """Test the status codes returned by all the apis under test"""
    response = requests.request(verb,path,json=body)
    assert response.status_code == statuscode


@pytest.mark.content_type
# @pytest.mark.xfail()
@pytest.mark.parametrize("path,verb,body,statuscode",
[
(f"{api_url}{users_api}","GET",None,200),
(f"{api_url}{users_api}/2","GET",None,200),
(f"{api_url}{users_api}/24","GET",None,404),
(f"{api_url}{unknown_api}","GET",None,200),
(f"{api_url}{unknown_api}/2","GET",None,200),
(f"{api_url}{unknown_api}/25","GET",None,404),
(f"{api_url}{users_api}","POST",{"name": "morpheus", "job": "leader"},201),
(f"{api_url}{users_api}/2","PUT",{"name": "morpheus", "job": "zion resident"},200),
(f"{api_url}{users_api}/2","PATCH",{"name": "morpheus", "job": "zion resident"},200),
(f"{api_url}{users_api}/2","DELETE",None,204),
(f"{api_url}{register_api}","POST",{"email": "eve.holt@reqres.in","password": "cityslicka"},200),
(f"{api_url}{register_api}","POST",{"password": "pistol"},400),
(f"{api_url}{register_api}","POST",{"email": "peter@klaven"},400),
(f"{api_url}{login_api}","POST",{"email": "eve.holt@reqres.in","password": "cityslicka"},200),
(f"{api_url}{login_api}","POST",{"password": "pistol"},400),
(f"{api_url}{login_api}","POST",{"email": "peter@klaven"},400),
(f"{api_url}{users_api}?delay=3","GET",None,200),
])
@pytest.mark.content_type1
def test_content_type_returned(path,verb,body,statuscode):
    """Verify the content-type returned by all the apis under test is 'application/json; charset=utf-8'"""
    response = requests.request(verb,path,json=body)
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"


@pytest.mark.parametrize("page,per_page,result",
[
    (1,1,1),
    (1,4,4),
    (2,4,4),
    (1,7,7),
    (2,7,5),
    (1,12,12),
    (2,12,0),
    (2,15,0),
])
def test_items_per_page(page,per_page,result):
    """ 
    WHEN I set items_per_page to 2 in GET /api/users
    THEN only 2 user info should be returned for each page
    """
    api_params = {"page":page,"per_page":per_page}
    response = requests.get(f"{api_url}{users_api}", params=api_params)
    res_json = response.json()
    assert response.status_code == 200
    assert res_json["page"] == page
    assert res_json["per_page"] == per_page
    assert len(res_json["data"]) == result

def test_docker():
    url = "http://localhost:80"
    resp = requests.get(url)
    print(resp.status_code)
    assert resp.ok is True