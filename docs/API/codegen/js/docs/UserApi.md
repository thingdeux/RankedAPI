# RankedApi.UserApi

All URIs are relative to *http://dev.goranked.com/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**addNewFollowers**](UserApi.md#addNewFollowers) | **POST** /users/{user_id}/friends | Follow a user
[**authorizeUser**](UserApi.md#authorizeUser) | **POST** /users/auth | OAuth Authorization Endpoint for already registered users.
[**getCurrentUserDetails**](UserApi.md#getCurrentUserDetails) | **GET** /users/me | Returns authorized users information
[**getFriends**](UserApi.md#getFriends) | **GET** /users/{user_id}/friends | List a given users&#39; followed friends
[**getUserDetails**](UserApi.md#getUserDetails) | **GET** /users/{user_id} | Returns a user queried by id
[**registerUser**](UserApi.md#registerUser) | **POST** /users/register | User Registration Endpoint
[**stopFollowingUser**](UserApi.md#stopFollowingUser) | **DELETE** /users/{user_id}/friends | Stop Following a user
[**updateUserDetails**](UserApi.md#updateUserDetails) | **PUT** /users/{user_id} | Update a Users information


<a name="addNewFollowers"></a>
# **addNewFollowers**
> addNewFollowers(userId)

Follow a user

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.UserApi();

var userId = 56; // Number | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.addNewFollowers(userId, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **userId** | **Number**|  | 

### Return type

null (empty response body)

### Authorization

[ranked_auth](../README.md#ranked_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="authorizeUser"></a>
# **authorizeUser**
> UserAuth authorizeUser(grantType, username, password)

OAuth Authorization Endpoint for already registered users.

### Example
```javascript
var RankedApi = require('ranked_api');

var apiInstance = new RankedApi.UserApi();

var grantType = "grantType_example"; // String | 

var username = "username_example"; // String | 

var password = "password_example"; // String | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.authorizeUser(grantType, username, password, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **grantType** | **String**|  | 
 **username** | **String**|  | 
 **password** | **String**|  | 

### Return type

[**UserAuth**](UserAuth.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: application/json

<a name="getCurrentUserDetails"></a>
# **getCurrentUserDetails**
> User getCurrentUserDetails()

Returns authorized users information

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.UserApi();

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.getCurrentUserDetails(callback);
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**User**](User.md)

### Authorization

[ranked_auth](../README.md#ranked_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a name="getFriends"></a>
# **getFriends**
> UserList getFriends()

List a given users&#39; followed friends

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.UserApi();

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.getFriends(callback);
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**UserList**](UserList.md)

### Authorization

[ranked_auth](../README.md#ranked_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getUserDetails"></a>
# **getUserDetails**
> User getUserDetails(userId)

Returns a user queried by id

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.UserApi();

var userId = 789; // Number | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.getUserDetails(userId, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **userId** | **Number**|  | 

### Return type

[**User**](User.md)

### Authorization

[ranked_auth](../README.md#ranked_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a name="registerUser"></a>
# **registerUser**
> UserAuth registerUser(username, email, password, unlockKey, opts)

User Registration Endpoint

### Example
```javascript
var RankedApi = require('ranked_api');

var apiInstance = new RankedApi.UserApi();

var username = "username_example"; // String | 

var email = "email_example"; // String | 

var password = "password_example"; // String | 

var unlockKey = "unlockKey_example"; // String | 

var opts = { 
  'phoneNumber': "phoneNumber_example" // String | 
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.registerUser(username, email, password, unlockKey, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **String**|  | 
 **email** | **String**|  | 
 **password** | **String**|  | 
 **unlockKey** | **String**|  | 
 **phoneNumber** | **String**|  | [optional] 

### Return type

[**UserAuth**](UserAuth.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: application/json

<a name="stopFollowingUser"></a>
# **stopFollowingUser**
> stopFollowingUser(userId)

Stop Following a user

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.UserApi();

var userId = 789; // Number | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.stopFollowingUser(userId, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **userId** | **Number**|  | 

### Return type

null (empty response body)

### Authorization

[ranked_auth](../README.md#ranked_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateUserDetails"></a>
# **updateUserDetails**
> User updateUserDetails(userId, email, password)

Update a Users information

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.UserApi();

var userId = 56; // Number | 

var email = "email_example"; // String | Users' E-Mail address

var password = "password_example"; // String | Users' Password


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.updateUserDetails(userId, email, password, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **userId** | **Number**|  | 
 **email** | **String**| Users&#39; E-Mail address | 
 **password** | **String**| Users&#39; Password | 

### Return type

[**User**](User.md)

### Authorization

[ranked_auth](../README.md#ranked_auth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded
 - **Accept**: application/json

