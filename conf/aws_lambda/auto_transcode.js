"use strict";

var AWS = require("aws-sdk");
var s3 = new AWS.S3({
 apiVersion: "2012–09–25"
});

var eltr = new AWS.ElasticTranscoder({
 apiVersion: "2012–09–25",
 region: "us-west-2"
});

exports.handler = function(event, context) {
 console.log("Generating Elastic Transcoder Job");
 var bucket = event.Records[0].s3.bucket.name;
 var key = event.Records[0].s3.object.key;
 var pipelineId = "1496812035419-5s3jr8";
 if (bucket !== "ranked-video-upload") {
  context.fail("Incorrect Video Input Bucket");
  return;
 }
 var srcKey =  decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, " ")); // the object may have spaces
 var newKey = key.split(".")[0];
 var params = {
  PipelineId: pipelineId,
  Input: {
   Key: srcKey,
   FrameRate: "auto",
   Resolution: "auto",
   AspectRatio: "auto",
   Interlaced: "auto",
   Container: "auto"
  },
  Outputs: [{
   Key: newKey + ".mp4",
   ThumbnailPattern: newKey + "-{count}",
   PresetId: "1499652501062-cjnh3u" // RankedWebMp41By1 PNG
  },{
   Key: newKey + ".webm",
   ThumbnailPattern: "",
   PresetId: "1351620000001-100240" // Webm 720p
  }]
 };
 console.log("Starting Job");
 eltr.createJob(params, function(err, data){
  if (err){
   console.log(err);
  } else {
   console.log(data);
  }
  context.succeed("Job well done");
 });
};