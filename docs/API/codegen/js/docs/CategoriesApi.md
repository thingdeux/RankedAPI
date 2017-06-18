# RankedApi.CategoriesApi

All URIs are relative to *http://dev.goranked.com/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**listCategories**](CategoriesApi.md#listCategories) | **GET** /categories/ | List of available categories / sub-categories


<a name="listCategories"></a>
# **listCategories**
> listCategories(authorization)

List of available categories / sub-categories

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.CategoriesApi();

var authorization = "authorization_example"; // String | Required Authorization Bearer Token for OAuth2


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.listCategories(authorization, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**| Required Authorization Bearer Token for OAuth2 | 

### Return type

null (empty response body)

### Authorization

[ranked_auth](../README.md#ranked_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

