# RankedApi.SearchApi

All URIs are relative to *http://dev.goranked.com/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getSearchResults**](SearchApi.md#getSearchResults) | **GET** /search | Search for Content


<a name="getSearchResults"></a>
# **getSearchResults**
> SearchResult getSearchResults(opts)

Search for Content

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.SearchApi();

var opts = { 
  'category': "category_example", // String | Search by specific category. ex: \"Food\"
  'subCategory': "subCategory_example", // String | Search by specific sub-category. ex: Latin
  'types': "types_example", // String | Comma delimited list of search result types (see models re: Search Types). ex: Video,Users
  'sort': "sort_example" // String | NOTE: Ignored for Alpha - always top - sort order (see models re: Sort Criteria)
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.getSearchResults(opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **category** | **String**| Search by specific category. ex: \&quot;Food\&quot; | [optional] 
 **subCategory** | **String**| Search by specific sub-category. ex: Latin | [optional] 
 **types** | **String**| Comma delimited list of search result types (see models re: Search Types). ex: Video,Users | [optional] 
 **sort** | **String**| NOTE: Ignored for Alpha - always top - sort order (see models re: Sort Criteria) | [optional] 

### Return type

[**SearchResult**](SearchResult.md)

### Authorization

[ranked_auth](../README.md#ranked_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

