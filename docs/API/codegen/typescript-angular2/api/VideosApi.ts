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
 */

import { Inject, Injectable, Optional }                      from '@angular/core';
import { Http, Headers, URLSearchParams }                    from '@angular/http';
import { RequestMethod, RequestOptions, RequestOptionsArgs } from '@angular/http';
import { Response, ResponseContentType }                     from '@angular/http';

import { Observable }                                        from 'rxjs/Observable';
import 'rxjs/add/operator/map';

import * as models                                           from '../model/models';
import { BASE_PATH, COLLECTION_FORMATS }                     from '../variables';
import { Configuration }                                     from '../configuration';

/* tslint:disable:no-unused-variable member-ordering */


@Injectable()
export class VideosApi {
    protected basePath = 'http://dev.goranked.com/api/v1';
    public defaultHeaders: Headers = new Headers();
    public configuration: Configuration = new Configuration();

    constructor(protected http: Http, @Optional()@Inject(BASE_PATH) basePath: string, @Optional() configuration: Configuration) {
        if (basePath) {
            this.basePath = basePath;
        }
        if (configuration) {
            this.configuration = configuration;
        }
    }

    /**
     * &#39;Like&#39; or rank a given video
     * 
     * @param videoId Video ID to be ranked
     */
    public addVideoRank(videoId: number, extraHttpRequestParams?: any): Observable<{}> {
        return this.addVideoRankWithHttpInfo(videoId, extraHttpRequestParams)
            .map((response: Response) => {
                if (response.status === 204) {
                    return undefined;
                } else {
                    return response.json();
                }
            });
    }

    /**
     * Comment on a given video
     * 
     * @param videoId Video ID to be commented upon
     * @param comment Comment to be left the video
     */
    public createVideoComment(videoId: number, comment?: string, extraHttpRequestParams?: any): Observable<{}> {
        return this.createVideoCommentWithHttpInfo(videoId, comment, extraHttpRequestParams)
            .map((response: Response) => {
                if (response.status === 204) {
                    return undefined;
                } else {
                    return response.json();
                }
            });
    }

    /**
     * List of top 20 most popular videos
     * 
     */
    public getTopVideos(extraHttpRequestParams?: any): Observable<models.VideoList> {
        return this.getTopVideosWithHttpInfo(extraHttpRequestParams)
            .map((response: Response) => {
                if (response.status === 204) {
                    return undefined;
                } else {
                    return response.json();
                }
            });
    }

    /**
     * Detailed information about one video
     * 
     * @param videoId Ranked Video Detail Resource - All details on a given video
     */
    public getVideoDetails(videoId: number, extraHttpRequestParams?: any): Observable<models.VideoDetail> {
        return this.getVideoDetailsWithHttpInfo(videoId, extraHttpRequestParams)
            .map((response: Response) => {
                if (response.status === 204) {
                    return undefined;
                } else {
                    return response.json();
                }
            });
    }

    /**
     * Endpoint to handle video uploads
     * 
     * @param filename name of file being uploaded
     */
    public initVideoUpload(filename: string, extraHttpRequestParams?: any): Observable<models.VideoUploadDetails> {
        return this.initVideoUploadWithHttpInfo(filename, extraHttpRequestParams)
            .map((response: Response) => {
                if (response.status === 204) {
                    return undefined;
                } else {
                    return response.json();
                }
            });
    }

    /**
     * &#39;Dislike&#39; or de-rank a given video
     * 
     * @param videoId Video ID to unrank
     */
    public removeVideRank(videoId: number, extraHttpRequestParams?: any): Observable<{}> {
        return this.removeVideRankWithHttpInfo(videoId, extraHttpRequestParams)
            .map((response: Response) => {
                if (response.status === 204) {
                    return undefined;
                } else {
                    return response.json();
                }
            });
    }

    /**
     * Delete personal videos from Ranked
     * 
     * @param videoId Ranked Video Detail Resource - All details on a given video
     */
    public removeVideo(videoId: number, extraHttpRequestParams?: any): Observable<{}> {
        return this.removeVideoWithHttpInfo(videoId, extraHttpRequestParams)
            .map((response: Response) => {
                if (response.status === 204) {
                    return undefined;
                } else {
                    return response.json();
                }
            });
    }

    /**
     * Update an existing Video
     * 
     * @param videoId 
     * @param title Title of the video
     * @param category String name for valid category
     * @param subCategory String name for valid sub-category
     */
    public updateVideoDetails(videoId: number, title?: string, category?: string, subCategory?: string, extraHttpRequestParams?: any): Observable<models.Video> {
        return this.updateVideoDetailsWithHttpInfo(videoId, title, category, subCategory, extraHttpRequestParams)
            .map((response: Response) => {
                if (response.status === 204) {
                    return undefined;
                } else {
                    return response.json();
                }
            });
    }


    /**
     * &#39;Like&#39; or rank a given video
     * 
     * @param videoId Video ID to be ranked
     */
    public addVideoRankWithHttpInfo(videoId: number, extraHttpRequestParams?: any): Observable<Response> {
        const path = this.basePath + `/videos/${video_id}/rank/`;

        let queryParameters = new URLSearchParams();
        let headers = new Headers(this.defaultHeaders.toJSON()); // https://github.com/angular/angular/issues/6845
        // verify required parameter 'videoId' is not null or undefined
        if (videoId === null || videoId === undefined) {
            throw new Error('Required parameter videoId was null or undefined when calling addVideoRank.');
        }
        // to determine the Content-Type header
        let consumes: string[] = [
            'application/json'
        ];

        // to determine the Accept header
        let produces: string[] = [
            'application/json'
        ];

        // authentication (ranked_auth) required
        // oauth required
        if (this.configuration.accessToken) {
            let accessToken = typeof this.configuration.accessToken === 'function'
                ? this.configuration.accessToken()
                : this.configuration.accessToken;
            headers.set('Authorization', 'Bearer ' + accessToken);
        }

        let requestOptions: RequestOptionsArgs = new RequestOptions({
            method: RequestMethod.Post,
            headers: headers,
            search: queryParameters
        });

        // https://github.com/swagger-api/swagger-codegen/issues/4037
        if (extraHttpRequestParams) {
            requestOptions = (<any>Object).assign(requestOptions, extraHttpRequestParams);
        }

        return this.http.request(path, requestOptions);
    }

    /**
     * Comment on a given video
     * 
     * @param videoId Video ID to be commented upon
     * @param comment Comment to be left the video
     */
    public createVideoCommentWithHttpInfo(videoId: number, comment?: string, extraHttpRequestParams?: any): Observable<Response> {
        const path = this.basePath + `/videos/${video_id}/comments/`;

        let queryParameters = new URLSearchParams();
        let headers = new Headers(this.defaultHeaders.toJSON()); // https://github.com/angular/angular/issues/6845
        let formParams = new URLSearchParams();

        // verify required parameter 'videoId' is not null or undefined
        if (videoId === null || videoId === undefined) {
            throw new Error('Required parameter videoId was null or undefined when calling createVideoComment.');
        }
        // to determine the Content-Type header
        let consumes: string[] = [
            'application/json'
        ];

        // to determine the Accept header
        let produces: string[] = [
            'application/json'
        ];

        // authentication (ranked_auth) required
        // oauth required
        if (this.configuration.accessToken) {
            let accessToken = typeof this.configuration.accessToken === 'function'
                ? this.configuration.accessToken()
                : this.configuration.accessToken;
            headers.set('Authorization', 'Bearer ' + accessToken);
        }

        headers.set('Content-Type', 'application/x-www-form-urlencoded');

        if (comment !== undefined) {
            formParams.set('comment', <any>comment);
        }

        let requestOptions: RequestOptionsArgs = new RequestOptions({
            method: RequestMethod.Post,
            headers: headers,
            body: formParams.toString(),
            search: queryParameters
        });

        // https://github.com/swagger-api/swagger-codegen/issues/4037
        if (extraHttpRequestParams) {
            requestOptions = (<any>Object).assign(requestOptions, extraHttpRequestParams);
        }

        return this.http.request(path, requestOptions);
    }

    /**
     * List of top 20 most popular videos
     * 
     */
    public getTopVideosWithHttpInfo(extraHttpRequestParams?: any): Observable<Response> {
        const path = this.basePath + `/videos`;

        let queryParameters = new URLSearchParams();
        let headers = new Headers(this.defaultHeaders.toJSON()); // https://github.com/angular/angular/issues/6845
        // to determine the Content-Type header
        let consumes: string[] = [
        ];

        // to determine the Accept header
        let produces: string[] = [
            'application/json'
        ];

        // authentication (ranked_auth) required
        // oauth required
        if (this.configuration.accessToken) {
            let accessToken = typeof this.configuration.accessToken === 'function'
                ? this.configuration.accessToken()
                : this.configuration.accessToken;
            headers.set('Authorization', 'Bearer ' + accessToken);
        }

        let requestOptions: RequestOptionsArgs = new RequestOptions({
            method: RequestMethod.Get,
            headers: headers,
            search: queryParameters
        });

        // https://github.com/swagger-api/swagger-codegen/issues/4037
        if (extraHttpRequestParams) {
            requestOptions = (<any>Object).assign(requestOptions, extraHttpRequestParams);
        }

        return this.http.request(path, requestOptions);
    }

    /**
     * Detailed information about one video
     * 
     * @param videoId Ranked Video Detail Resource - All details on a given video
     */
    public getVideoDetailsWithHttpInfo(videoId: number, extraHttpRequestParams?: any): Observable<Response> {
        const path = this.basePath + `/videos/${video_id}`;

        let queryParameters = new URLSearchParams();
        let headers = new Headers(this.defaultHeaders.toJSON()); // https://github.com/angular/angular/issues/6845
        // verify required parameter 'videoId' is not null or undefined
        if (videoId === null || videoId === undefined) {
            throw new Error('Required parameter videoId was null or undefined when calling getVideoDetails.');
        }
        // to determine the Content-Type header
        let consumes: string[] = [
        ];

        // to determine the Accept header
        let produces: string[] = [
            'application/json'
        ];

        // authentication (ranked_auth) required
        // oauth required
        if (this.configuration.accessToken) {
            let accessToken = typeof this.configuration.accessToken === 'function'
                ? this.configuration.accessToken()
                : this.configuration.accessToken;
            headers.set('Authorization', 'Bearer ' + accessToken);
        }

        let requestOptions: RequestOptionsArgs = new RequestOptions({
            method: RequestMethod.Get,
            headers: headers,
            search: queryParameters
        });

        // https://github.com/swagger-api/swagger-codegen/issues/4037
        if (extraHttpRequestParams) {
            requestOptions = (<any>Object).assign(requestOptions, extraHttpRequestParams);
        }

        return this.http.request(path, requestOptions);
    }

    /**
     * Endpoint to handle video uploads
     * 
     * @param filename name of file being uploaded
     */
    public initVideoUploadWithHttpInfo(filename: string, extraHttpRequestParams?: any): Observable<Response> {
        const path = this.basePath + `/videos/upload`;

        let queryParameters = new URLSearchParams();
        let headers = new Headers(this.defaultHeaders.toJSON()); // https://github.com/angular/angular/issues/6845
        let formParams = new URLSearchParams();

        // verify required parameter 'filename' is not null or undefined
        if (filename === null || filename === undefined) {
            throw new Error('Required parameter filename was null or undefined when calling initVideoUpload.');
        }
        // to determine the Content-Type header
        let consumes: string[] = [
        ];

        // to determine the Accept header
        let produces: string[] = [
            'application/json'
        ];

        // authentication (ranked_auth) required
        // oauth required
        if (this.configuration.accessToken) {
            let accessToken = typeof this.configuration.accessToken === 'function'
                ? this.configuration.accessToken()
                : this.configuration.accessToken;
            headers.set('Authorization', 'Bearer ' + accessToken);
        }

        headers.set('Content-Type', 'application/x-www-form-urlencoded');

        if (filename !== undefined) {
            formParams.set('filename', <any>filename);
        }

        let requestOptions: RequestOptionsArgs = new RequestOptions({
            method: RequestMethod.Post,
            headers: headers,
            body: formParams.toString(),
            search: queryParameters
        });

        // https://github.com/swagger-api/swagger-codegen/issues/4037
        if (extraHttpRequestParams) {
            requestOptions = (<any>Object).assign(requestOptions, extraHttpRequestParams);
        }

        return this.http.request(path, requestOptions);
    }

    /**
     * &#39;Dislike&#39; or de-rank a given video
     * 
     * @param videoId Video ID to unrank
     */
    public removeVideRankWithHttpInfo(videoId: number, extraHttpRequestParams?: any): Observable<Response> {
        const path = this.basePath + `/videos/${video_id}/rank/`;

        let queryParameters = new URLSearchParams();
        let headers = new Headers(this.defaultHeaders.toJSON()); // https://github.com/angular/angular/issues/6845
        // verify required parameter 'videoId' is not null or undefined
        if (videoId === null || videoId === undefined) {
            throw new Error('Required parameter videoId was null or undefined when calling removeVideRank.');
        }
        // to determine the Content-Type header
        let consumes: string[] = [
            'application/json'
        ];

        // to determine the Accept header
        let produces: string[] = [
            'application/json'
        ];

        // authentication (ranked_auth) required
        // oauth required
        if (this.configuration.accessToken) {
            let accessToken = typeof this.configuration.accessToken === 'function'
                ? this.configuration.accessToken()
                : this.configuration.accessToken;
            headers.set('Authorization', 'Bearer ' + accessToken);
        }

        let requestOptions: RequestOptionsArgs = new RequestOptions({
            method: RequestMethod.Delete,
            headers: headers,
            search: queryParameters
        });

        // https://github.com/swagger-api/swagger-codegen/issues/4037
        if (extraHttpRequestParams) {
            requestOptions = (<any>Object).assign(requestOptions, extraHttpRequestParams);
        }

        return this.http.request(path, requestOptions);
    }

    /**
     * Delete personal videos from Ranked
     * 
     * @param videoId Ranked Video Detail Resource - All details on a given video
     */
    public removeVideoWithHttpInfo(videoId: number, extraHttpRequestParams?: any): Observable<Response> {
        const path = this.basePath + `/videos/${video_id}`;

        let queryParameters = new URLSearchParams();
        let headers = new Headers(this.defaultHeaders.toJSON()); // https://github.com/angular/angular/issues/6845
        // verify required parameter 'videoId' is not null or undefined
        if (videoId === null || videoId === undefined) {
            throw new Error('Required parameter videoId was null or undefined when calling removeVideo.');
        }
        // to determine the Content-Type header
        let consumes: string[] = [
        ];

        // to determine the Accept header
        let produces: string[] = [
            'application/json'
        ];

        // authentication (ranked_auth) required
        // oauth required
        if (this.configuration.accessToken) {
            let accessToken = typeof this.configuration.accessToken === 'function'
                ? this.configuration.accessToken()
                : this.configuration.accessToken;
            headers.set('Authorization', 'Bearer ' + accessToken);
        }

        let requestOptions: RequestOptionsArgs = new RequestOptions({
            method: RequestMethod.Delete,
            headers: headers,
            search: queryParameters
        });

        // https://github.com/swagger-api/swagger-codegen/issues/4037
        if (extraHttpRequestParams) {
            requestOptions = (<any>Object).assign(requestOptions, extraHttpRequestParams);
        }

        return this.http.request(path, requestOptions);
    }

    /**
     * Update an existing Video
     * 
     * @param videoId 
     * @param title Title of the video
     * @param category String name for valid category
     * @param subCategory String name for valid sub-category
     */
    public updateVideoDetailsWithHttpInfo(videoId: number, title?: string, category?: string, subCategory?: string, extraHttpRequestParams?: any): Observable<Response> {
        const path = this.basePath + `/videos/${video_id}`;

        let queryParameters = new URLSearchParams();
        let headers = new Headers(this.defaultHeaders.toJSON()); // https://github.com/angular/angular/issues/6845
        let formParams = new URLSearchParams();

        // verify required parameter 'videoId' is not null or undefined
        if (videoId === null || videoId === undefined) {
            throw new Error('Required parameter videoId was null or undefined when calling updateVideoDetails.');
        }
        // to determine the Content-Type header
        let consumes: string[] = [
            'application/json'
        ];

        // to determine the Accept header
        let produces: string[] = [
            'application/json'
        ];

        // authentication (ranked_auth) required
        // oauth required
        if (this.configuration.accessToken) {
            let accessToken = typeof this.configuration.accessToken === 'function'
                ? this.configuration.accessToken()
                : this.configuration.accessToken;
            headers.set('Authorization', 'Bearer ' + accessToken);
        }

        headers.set('Content-Type', 'application/x-www-form-urlencoded');

        if (title !== undefined) {
            formParams.set('title', <any>title);
        }

        if (category !== undefined) {
            formParams.set('category', <any>category);
        }

        if (subCategory !== undefined) {
            formParams.set('sub_category', <any>subCategory);
        }

        let requestOptions: RequestOptionsArgs = new RequestOptions({
            method: RequestMethod.Put,
            headers: headers,
            body: formParams.toString(),
            search: queryParameters
        });

        // https://github.com/swagger-api/swagger-codegen/issues/4037
        if (extraHttpRequestParams) {
            requestOptions = (<any>Object).assign(requestOptions, extraHttpRequestParams);
        }

        return this.http.request(path, requestOptions);
    }

}
