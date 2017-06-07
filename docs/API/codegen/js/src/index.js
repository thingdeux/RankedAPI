/**
 * Ranked API
 * API for mobile and/or Web Clients
 *
 * OpenAPI spec version: 0.0.8
 * Contact: me@josh.land
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 * Do not edit the class manually.
 *
 */

(function(factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module.
    define(['ApiClient', 'model/Comment', 'model/SearchResult', 'model/SearchTypes', 'model/SortCriteria', 'model/User', 'model/UserAuth', 'model/UserList', 'model/Video', 'model/VideoDetail', 'model/VideoList', 'model/VideoQualityOptions', 'model/VideoUploadDetails', 'api/SearchApi', 'api/UserApi', 'api/VideosApi'], factory);
  } else if (typeof module === 'object' && module.exports) {
    // CommonJS-like environments that support module.exports, like Node.
    module.exports = factory(require('./ApiClient'), require('./model/Comment'), require('./model/SearchResult'), require('./model/SearchTypes'), require('./model/SortCriteria'), require('./model/User'), require('./model/UserAuth'), require('./model/UserList'), require('./model/Video'), require('./model/VideoDetail'), require('./model/VideoList'), require('./model/VideoQualityOptions'), require('./model/VideoUploadDetails'), require('./api/SearchApi'), require('./api/UserApi'), require('./api/VideosApi'));
  }
}(function(ApiClient, Comment, SearchResult, SearchTypes, SortCriteria, User, UserAuth, UserList, Video, VideoDetail, VideoList, VideoQualityOptions, VideoUploadDetails, SearchApi, UserApi, VideosApi) {
  'use strict';

  /**
   * API_for_mobile_andor_Web_Clients.<br>
   * The <code>index</code> module provides access to constructors for all the classes which comprise the public API.
   * <p>
   * An AMD (recommended!) or CommonJS application will generally do something equivalent to the following:
   * <pre>
   * var RankedApi = require('index'); // See note below*.
   * var xxxSvc = new RankedApi.XxxApi(); // Allocate the API class we're going to use.
   * var yyyModel = new RankedApi.Yyy(); // Construct a model instance.
   * yyyModel.someProperty = 'someValue';
   * ...
   * var zzz = xxxSvc.doSomething(yyyModel); // Invoke the service.
   * ...
   * </pre>
   * <em>*NOTE: For a top-level AMD script, use require(['index'], function(){...})
   * and put the application logic within the callback function.</em>
   * </p>
   * <p>
   * A non-AMD browser application (discouraged) might do something like this:
   * <pre>
   * var xxxSvc = new RankedApi.XxxApi(); // Allocate the API class we're going to use.
   * var yyy = new RankedApi.Yyy(); // Construct a model instance.
   * yyyModel.someProperty = 'someValue';
   * ...
   * var zzz = xxxSvc.doSomething(yyyModel); // Invoke the service.
   * ...
   * </pre>
   * </p>
   * @module index
   * @version 0.0.8
   */
  var exports = {
    /**
     * The ApiClient constructor.
     * @property {module:ApiClient}
     */
    ApiClient: ApiClient,
    /**
     * The Comment model constructor.
     * @property {module:model/Comment}
     */
    Comment: Comment,
    /**
     * The SearchResult model constructor.
     * @property {module:model/SearchResult}
     */
    SearchResult: SearchResult,
    /**
     * The SearchTypes model constructor.
     * @property {module:model/SearchTypes}
     */
    SearchTypes: SearchTypes,
    /**
     * The SortCriteria model constructor.
     * @property {module:model/SortCriteria}
     */
    SortCriteria: SortCriteria,
    /**
     * The User model constructor.
     * @property {module:model/User}
     */
    User: User,
    /**
     * The UserAuth model constructor.
     * @property {module:model/UserAuth}
     */
    UserAuth: UserAuth,
    /**
     * The UserList model constructor.
     * @property {module:model/UserList}
     */
    UserList: UserList,
    /**
     * The Video model constructor.
     * @property {module:model/Video}
     */
    Video: Video,
    /**
     * The VideoDetail model constructor.
     * @property {module:model/VideoDetail}
     */
    VideoDetail: VideoDetail,
    /**
     * The VideoList model constructor.
     * @property {module:model/VideoList}
     */
    VideoList: VideoList,
    /**
     * The VideoQualityOptions model constructor.
     * @property {module:model/VideoQualityOptions}
     */
    VideoQualityOptions: VideoQualityOptions,
    /**
     * The VideoUploadDetails model constructor.
     * @property {module:model/VideoUploadDetails}
     */
    VideoUploadDetails: VideoUploadDetails,
    /**
     * The SearchApi service constructor.
     * @property {module:api/SearchApi}
     */
    SearchApi: SearchApi,
    /**
     * The UserApi service constructor.
     * @property {module:api/UserApi}
     */
    UserApi: UserApi,
    /**
     * The VideosApi service constructor.
     * @property {module:api/VideosApi}
     */
    VideosApi: VideosApi
  };

  return exports;
}));
