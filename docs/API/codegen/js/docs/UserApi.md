# RankedApi.UserApi

All URIs are relative to *http://dev.goranked.com/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**addNewFollowers**](UserApi.md#addNewFollowers) | **POST** /users/{user_id}/friends | Follow a user
[**authorizeUser**](UserApi.md#authorizeUser) | **POST** /users/auth/token | OAuth Authorization Endpoint for already registered users.
[**getCurrentUserDetails**](UserApi.md#getCurrentUserDetails) | **GET** /users/me | Returns authorized users information
[**getFriends**](UserApi.md#getFriends) | **GET** /users/{user_id}/friends | List a given users&#39; followed friends
[**getUserDetails**](UserApi.md#getUserDetails) | **GET** /users/{user_id} | Returns a user queried by id
[**registerUser**](UserApi.md#registerUser) | **POST** /users/register | User Registration Endpoint
[**stopFollowingUser**](UserApi.md#stopFollowingUser) | **DELETE** /users/{user_id}/friends | Stop Following a user
[**updateUserDetailPatch**](UserApi.md#updateUserDetailPatch) | **PATCH** /users/{user_id} | Update one or more fields of a Users&#39; profile
[**updateUserDetails**](UserApi.md#updateUserDetails) | **PUT** /users/{user_id} | Update a Users information
[**uploadAvatar**](UserApi.md#uploadAvatar) | **PUT** /users/{user_id}/avatar | Upload an avatar image file.


<a name="addNewFollowers"></a>
# **addNewFollowers**
> addNewFollowers(authorization, userId)

Follow a user

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.UserApi();

var authorization = "authorization_example"; // String | Required Authorization Bearer Token for OAuth2

var userId = 56; // Number | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.addNewFollowers(authorization, userId, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**| Required Authorization Bearer Token for OAuth2 | 
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
> UserAuth authorizeUser(grantType, username, password, clientId)

OAuth Authorization Endpoint for already registered users.

### Example
```javascript
var RankedApi = require('ranked_api');

var apiInstance = new RankedApi.UserApi();

var grantType = "grantType_example"; // String | 

var username = "username_example"; // String | 

var password = "password_example"; // String | 

var clientId = "clientId_example"; // String | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.authorizeUser(grantType, username, password, clientId, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **grantType** | **String**|  | 
 **username** | **String**|  | 
 **password** | **String**|  | 
 **clientId** | **String**|  | 

### Return type

[**UserAuth**](UserAuth.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getCurrentUserDetails"></a>
# **getCurrentUserDetails**
> User getCurrentUserDetails(authorization)

Returns authorized users information

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.UserApi();

var authorization = "authorization_example"; // String | Required Authorization Bearer Token for OAuth2


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.getCurrentUserDetails(authorization, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**| Required Authorization Bearer Token for OAuth2 | 

### Return type

[**User**](User.md)

### Authorization

[ranked_auth](../README.md#ranked_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a name="getFriends"></a>
# **getFriends**
> UserList getFriends(authorization)

List a given users&#39; followed friends

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.UserApi();

var authorization = "authorization_example"; // String | Required Authorization Bearer Token for OAuth2


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.getFriends(authorization, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**| Required Authorization Bearer Token for OAuth2 | 

### Return type

[**UserList**](UserList.md)

### Authorization

[ranked_auth](../README.md#ranked_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getUserDetails"></a>
# **getUserDetails**
> User getUserDetails(authorization, userId)

Returns a user queried by id

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.UserApi();

var authorization = "authorization_example"; // String | Required Authorization Bearer Token for OAuth2

var userId = 789; // Number | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.getUserDetails(authorization, userId, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**| Required Authorization Bearer Token for OAuth2 | 
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
> User registerUser(username, email, password, unlockKey, opts)

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

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="stopFollowingUser"></a>
# **stopFollowingUser**
> stopFollowingUser(authorization, userId)

Stop Following a user

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.UserApi();

var authorization = "authorization_example"; // String | Required Authorization Bearer Token for OAuth2

var userId = 789; // Number | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.stopFollowingUser(authorization, userId, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**| Required Authorization Bearer Token for OAuth2 | 
 **userId** | **Number**|  | 

### Return type

null (empty response body)

### Authorization

[ranked_auth](../README.md#ranked_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateUserDetailPatch"></a>
# **updateUserDetailPatch**
> User updateUserDetailPatch(authorization, userId, opts)

Update one or more fields of a Users&#39; profile

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.UserApi();

var authorization = "authorization_example"; // String | Required Authorization Bearer Token for OAuth2

var userId = 56; // Number | 

var opts = { 
  'email': "email_example", // String | Users' E-Mail address
  'password': "password_example", // String | Users' Password
  'avatarUrl': "avatarUrl_example", // String | Avatar URL
  'phoneNumber': "phoneNumber_example" // String | Phone Number
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.updateUserDetailPatch(authorization, userId, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**| Required Authorization Bearer Token for OAuth2 | 
 **userId** | **Number**|  | 
 **email** | **String**| Users&#39; E-Mail address | [optional] 
 **password** | **String**| Users&#39; Password | [optional] 
 **avatarUrl** | **String**| Avatar URL | [optional] 
 **phoneNumber** | **String**| Phone Number | [optional] 

### Return type

[**User**](User.md)

### Authorization

[ranked_auth](../README.md#ranked_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateUserDetails"></a>
# **updateUserDetails**
> User updateUserDetails(authorization, userId, email, password)

Update a Users information

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.UserApi();

var authorization = "authorization_example"; // String | Required Authorization Bearer Token for OAuth2

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
apiInstance.updateUserDetails(authorization, userId, email, password, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**| Required Authorization Bearer Token for OAuth2 | 
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

<a name="uploadAvatar"></a>
# **uploadAvatar**
> User uploadAvatar(opts)

Upload an avatar image file.

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.UserApi();

var opts = { 
  'file': "/path/to/file.txt" // File | The file to upload [ Size should be under 1mb ]
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.uploadAvatar(opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **File**| The file to upload [ Size should be under 1mb ] | [optional] 

### Return type

[**User**](User.md)

### Authorization

[ranked_auth](../README.md#ranked_auth)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: Not defined

