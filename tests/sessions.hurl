POST http://localhost:5765/api/register
{
	"username": "diamondburned",
	"password": "very weak password"
}
HTTP 200
[Asserts]
jsonpath "$.username" == "diamondburned"

POST http://localhost:5765/api/login
{
	"username": "diamondburned",
	"password": "very weak password"
}
HTTP 200
[Asserts]
jsonpath "$.username" == "diamondburned"
[Captures]
token: jsonpath "$.token"

GET http://localhost:5765/api/users/me
Authorization: Bearer {{token}}
HTTP 200
[Asserts]
jsonpath "$.username" == "diamondburned"
jsonpath "$.password" not exists
