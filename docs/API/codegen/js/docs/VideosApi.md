# RankedApi.VideosApi

All URIs are relative to *http://dev.goranked.com/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**addVideoRank**](VideosApi.md#addVideoRank) | **POST** /videos/{video_id}/rank/ | &#39;Like&#39; or rank a given video
[**createVideoComment**](VideosApi.md#createVideoComment) | **POST** /videos/{video_id}/comments/ | Comment on a given video
[**getTopVideos**](VideosApi.md#getTopVideos) | **GET** /videos | List of top 20 most popular videos
[**getVideoDetails**](VideosApi.md#getVideoDetails) | **GET** /videos/{video_id} | Detailed information about one video
[**initVideoUpload**](VideosApi.md#initVideoUpload) | **POST** /videos/upload | Endpoint to handle video uploads
[**removeVideRank**](VideosApi.md#removeVideRank) | **DELETE** /videos/{video_id}/rank/ | &#39;Dislike&#39; or de-rank a given video
[**removeVideo**](VideosApi.md#removeVideo) | **DELETE** /videos/{video_id} | Delete personal videos from Ranked
[**updateVideoDetails**](VideosApi.md#updateVideoDetails) | **PUT** /videos/{video_id} | Update an existing Video


<a name="addVideoRank"></a>
# **addVideoRank**
> addVideoRank(authorization, videoId, rankAmount)

&#39;Like&#39; or rank a given video

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.VideosApi();

var authorization = "authorization_example"; // String | Required Authorization Bearer Token for OAuth2

var videoId = 56; // Number | Video ID to be ranked

var rankAmount = 56; // Number | Rank value between 1-10


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.addVideoRank(authorization, videoId, rankAmount, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**| Required Authorization Bearer Token for OAuth2 | 
 **videoId** | **Number**| Video ID to be ranked | 
 **rankAmount** | **Number**| Rank value between 1-10 | 

### Return type

null (empty response body)

### Authorization

[ranked_auth](../README.md#ranked_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="createVideoComment"></a>
# **createVideoComment**
> createVideoComment(authorization, videoId, opts)

Comment on a given video

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.VideosApi();

var authorization = "authorization_example"; // String | Required Authorization Bearer Token for OAuth2

var videoId = 56; // Number | Video ID to be commented upon

var opts = { 
  'comment': "comment_example" // String | Comment to be left the video
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.createVideoComment(authorization, videoId, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**| Required Authorization Bearer Token for OAuth2 | 
 **videoId** | **Number**| Video ID to be commented upon | 
 **comment** | **String**| Comment to be left the video | [optional] 

### Return type

null (empty response body)

### Authorization

[ranked_auth](../README.md#ranked_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getTopVideos"></a>
# **getTopVideos**
> VideoList getTopVideos(authorization)

List of top 20 most popular videos

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.VideosApi();

var authorization = "authorization_example"; // String | Required Authorization Bearer Token for OAuth2


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.getTopVideos(authorization, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**| Required Authorization Bearer Token for OAuth2 | 

### Return type

[**VideoList**](VideoList.md)

### Authorization

[ranked_auth](../README.md#ranked_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a name="getVideoDetails"></a>
# **getVideoDetails**
> VideoDetail getVideoDetails(authorization, videoId)

Detailed information about one video

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.VideosApi();

var authorization = "authorization_example"; // String | Required Authorization Bearer Token for OAuth2

var videoId = 56; // Number | Ranked Video Detail Resource - All details on a given video


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.getVideoDetails(authorization, videoId, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**| Required Authorization Bearer Token for OAuth2 | 
 **videoId** | **Number**| Ranked Video Detail Resource - All details on a given video | 

### Return type

[**VideoDetail**](VideoDetail.md)

### Authorization

[ranked_auth](../README.md#ranked_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a name="initVideoUpload"></a>
# **initVideoUpload**
> VideoUploadDetails initVideoUpload(authorization, filename, fileType)

Endpoint to handle video uploads

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.VideosApi();

var authorization = "authorization_example"; // String | Required Authorization Bearer Token for OAuth2

var filename = "filename_example"; // String | name of file being uploaded

var fileType = "fileType_example"; // String | File type of uploading video


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.initVideoUpload(authorization, filename, fileType, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**| Required Authorization Bearer Token for OAuth2 | 
 **filename** | **String**| name of file being uploaded | 
 **fileType** | **String**| File type of uploading video | 

### Return type

[**VideoUploadDetails**](VideoUploadDetails.md)

### Authorization

[ranked_auth](../README.md#ranked_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a name="removeVideRank"></a>
# **removeVideRank**
> removeVideRank(authorization, videoId)

&#39;Dislike&#39; or de-rank a given video

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.VideosApi();

var authorization = "authorization_example"; // String | Required Authorization Bearer Token for OAuth2

var videoId = 56; // Number | Video ID to unrank


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.removeVideRank(authorization, videoId, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**| Required Authorization Bearer Token for OAuth2 | 
 **videoId** | **Number**| Video ID to unrank | 

### Return type

null (empty response body)

### Authorization

[ranked_auth](../README.md#ranked_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="removeVideo"></a>
# **removeVideo**
> removeVideo(authorization, videoId)

Delete personal videos from Ranked

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.VideosApi();

var authorization = "authorization_example"; // String | Required Authorization Bearer Token for OAuth2

var videoId = 56; // Number | Ranked Video Detail Resource - All details on a given video


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.removeVideo(authorization, videoId, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**| Required Authorization Bearer Token for OAuth2 | 
 **videoId** | **Number**| Ranked Video Detail Resource - All details on a given video | 

### Return type

null (empty response body)

### Authorization

[ranked_auth](../README.md#ranked_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a name="updateVideoDetails"></a>
# **updateVideoDetails**
> Video updateVideoDetails(authorization, videoId, opts)

Update an existing Video

### Example
```javascript
var RankedApi = require('ranked_api');
var defaultClient = RankedApi.ApiClient.default;

// Configure OAuth2 access token for authorization: ranked_auth
var ranked_auth = defaultClient.authentications['ranked_auth'];
ranked_auth.accessToken = 'YOUR ACCESS TOKEN';

var apiInstance = new RankedApi.VideosApi();

var authorization = "authorization_example"; // String | Required Authorization Bearer Token for OAuth2

var videoId = 56; // Number | 

var opts = { 
  'title': "title_example", // String | Title of the video
  'category': "category_example", // String | String name for valid category
  'subCategory': "subCategory_example" // String | String name for valid sub-category
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.updateVideoDetails(authorization, videoId, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authorization** | **String**| Required Authorization Bearer Token for OAuth2 | 
 **videoId** | **Number**|  | 
 **title** | **String**| Title of the video | [optional] 
 **category** | **String**| String name for valid category | [optional] 
 **subCategory** | **String**| String name for valid sub-category | [optional] 

### Return type

[**Video**](Video.md)

### Authorization

[ranked_auth](../README.md#ranked_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

