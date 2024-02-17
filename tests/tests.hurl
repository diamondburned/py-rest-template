#
# Account creation
#

POST http://localhost:5765/api/register
{
	"email": "diamond@libdb.so",
	"password": "very weak password"
}
HTTP 200
[Asserts]
jsonpath "$.token" exists
jsonpath "$.user_id" exists
[Captures]
user_id: jsonpath "$.user_id"

POST http://localhost:5765/api/login
{
	"email": "diamond@libdb.so",
	"password": "very weak password"
}
HTTP 200
[Asserts]
jsonpath "$.token" exists
jsonpath "$.user_id" == {{user_id}}
[Captures]
token: jsonpath "$.token"

#
# Asset handling
#

POST http://localhost:5765/api/assets
Authorization: Bearer {{token}}
[MultipartFormData]
file: file,amogus.png;
alt: Red among us
HTTP 200
[Asserts]
jsonpath "$.hash" exists
jsonpath "$.alt" == "Red among us"
[Captures]
asset_hash: jsonpath "$.hash"

GET http://localhost:5765/api/assets/{{asset_hash}}
Authorization: Bearer {{token}}
HTTP 200
[Asserts]
header "Content-Type" == "image/png"
bytes count > 10

GET http://localhost:5765/api/assets/{{asset_hash}}/metadata
Authorization: Bearer {{token}}
HTTP 200
[Asserts]
jsonpath "$.alt" == "Red among us"
jsonpath "$.content_type" == "image/png"


#
# Current User testing
#

GET http://localhost:5765/api/users/me
Authorization: Bearer {{token}}
HTTP 200
[Asserts]
jsonpath "$.id" == {{user_id}}
jsonpath "$.email" == "diamond@libdb.so"

PATCH http://localhost:5765/api/users/me
Authorization: Bearer {{token}}
{
	"email": "me@diamondx.pet",
	"password": "not so weak password",
	"avatar_hash": "{{asset_hash}}",
	"display_name": "Diamond"
}
HTTP 200
[Asserts]
jsonpath "$.id" == {{user_id}}
jsonpath "$.email" == "me@diamondx.pet"
jsonpath "$.avatar_hash" == {{asset_hash}}
jsonpath "$.display_name" == "Diamond"
