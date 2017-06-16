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
    instance = new RankedApi.Category();
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

  describe('Category', function() {
    it('should create an instance of Category', function() {
      // uncomment below and update the code to test Category
      //var instane = new RankedApi.Category();
      //expect(instance).to.be.a(RankedApi.Category);
    });

    it('should have the property id (base name: "id")', function() {
      // uncomment below and update the code to test the property id
      //var instane = new RankedApi.Category();
      //expect(instance).to.be();
    });

    it('should have the property name (base name: "name")', function() {
      // uncomment below and update the code to test the property name
      //var instane = new RankedApi.Category();
      //expect(instance).to.be();
    });

    it('should have the property parentCategory (base name: "parent_category")', function() {
      // uncomment below and update the code to test the property parentCategory
      //var instane = new RankedApi.Category();
      //expect(instance).to.be();
    });

    it('should have the property isSubCategory (base name: "is_sub_category")', function() {
      // uncomment below and update the code to test the property isSubCategory
      //var instane = new RankedApi.Category();
      //expect(instance).to.be();
    });

  });

}));
