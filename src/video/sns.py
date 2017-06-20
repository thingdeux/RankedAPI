import json


class SNSResponse:
    def __init__(self, raw_response):
        response_json = json.loads(str(raw_response, 'utf-8'))
        try:
            self.parse_sns_response(json.loads(response_json['Message']))
        except (KeyError, IndexError):
            self.state = ""
            self.processed_filename = ""

    def parse_sns_response(self, message_dict):
        """
            Parse the response that comes back from SNS

            Example Output of the dict-str in 'Message' - Excluding keys we care little about:
            {
              "state" : "COMPLETED",
              "version" : "2012-09-25",
              "jobId" : "1497930136953-0zif1n",
              "pipelineId" : "1496812035419-5s3jr8",
              "input" : {
                "key" : "1-197f3201-3a75-400a-87ae-c2af1a382fd5-sillytestvid.mp4"
              },
              "inputCount" : 1,
              "outputs" : [ {
                "id" : "1",
                "key" : "1-197f3201-3a75-400a-87ae-c2af1a382fd5-sillytestvid.mp4",
                "thumbnailPattern" : "1-197f3201-3a75-400a-87ae-c2af1a382fd5-sillytestvid-{count}",
                "status" : "Complete",
                "width" : 640,
                "height" : 360
              }, {
                "id" : "2",
                "key" : "1-197f3201-3a75-400a-87ae-c2af1a382fd5-sillytestvid.webm",
                "thumbnailPattern" : "",
                "status" : "Complete",
                "width" : 640,
                "height" : 360
              } ]
            }
        """
        self.state = message_dict['state']
        self.processed_filename = message_dict['input']['key']
        self.job_id = message_dict['jobId']
