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

(function(root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD.
    define(['expect.js', '../../src/index'], factory);
  } else if (typeof module === 'object' && module.exports) {
    // CommonJS-like environments that support module.exports, like Node.
    factory(require('expect.js'), require('../../src/index'));
  } else {
    // Browser globals (root is window)
    factory(root.expect, root.RankedApi);
  }
}(this, function(expect, RankedApi) {
  'use strict';

  var instance;

  beforeEach(function() {
    instance = new RankedApi.UserApi();
  });

  var getProperty = function(object, getter, property) {
    // Use getter method if present; otherwise, get the property directly.
    if (typeof object[getter] === 'function')
      return object[getter]();
    else
      return object[property];
  }

  var setProperty = function(object, setter, property, value) {
    // Use setter method if present; otherwise, set the property directly.
    if (typeof object[setter] === 'function')
      object[setter](value);
    else
      object[property] = value;
  }

  describe('UserApi', function() {
    describe('addNewFollowers', function() {
      it('should call addNewFollowers successfully', function(done) {
        //uncomment below and update the code to test addNewFollowers
        //instance.addNewFollowers(function(error) {
        //  if (error) throw error;
        //expect().to.be();
        //});
        done();
      });
    });
    describe('authorizeUser', function() {
      it('should call authorizeUser successfully', function(done) {
        //uncomment below and update the code to test authorizeUser
        //instance.authorizeUser(function(error) {
        //  if (error) throw error;
        //expect().to.be();
        //});
        done();
      });
    });
    describe('getCurrentUserDetails', function() {
      it('should call getCurrentUserDetails successfully', function(done) {
        //uncomment below and update the code to test getCurrentUserDetails
        //instance.getCurrentUserDetails(function(error) {
        //  if (error) throw error;
        //expect().to.be();
        //});
        done();
      });
    });
    describe('getFriends', function() {
      it('should call getFriends successfully', function(done) {
        //uncomment below and update the code to test getFriends
        //instance.getFriends(function(error) {
        //  if (error) throw error;
        //expect().to.be();
        //});
        done();
      });
    });
    describe('getUserDetails', function() {
      it('should call getUserDetails successfully', function(done) {
        //uncomment below and update the code to test getUserDetails
        //instance.getUserDetails(function(error) {
        //  if (error) throw error;
        //expect().to.be();
        //});
        done();
      });
    });
    describe('registerUser', function() {
      it('should call registerUser successfully', function(done) {
        //uncomment below and update the code to test registerUser
        //instance.registerUser(function(error) {
        //  if (error) throw error;
        //expect().to.be();
        //});
        done();
      });
    });
    describe('stopFollowingUser', function() {
      it('should call stopFollowingUser successfully', function(done) {
        //uncomment below and update the code to test stopFollowingUser
        //instance.stopFollowingUser(function(error) {
        //  if (error) throw error;
        //expect().to.be();
        //});
        done();
      });
    });
    describe('updateUserDetails', function() {
      it('should call updateUserDetails successfully', function(done) {
        //uncomment below and update the code to test updateUserDetails
        //instance.updateUserDetails(function(error) {
        //  if (error) throw error;
        //expect().to.be();
        //});
        done();
      });
    });
  });

}));