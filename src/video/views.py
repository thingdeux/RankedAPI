# Generate Video Presigned Note
# def sign_s3():
#   S3_BUCKET = os.environ.get('S3_BUCKET')
#
#   file_name = request.args.get('file_name')
#   file_type = request.args.get('file_type')
#
#   s3 = boto3.client('s3')
#
#   presigned_post = s3.generate_presigned_post(
#     Bucket = S3_BUCKET,
#     Key = file_name,
#     Fields = {"acl": "public-read", "Content-Type": file_type},
#     Conditions = [
#       {"acl": "public-read"},
#       {"Content-Type": file_type}
#     ],
#     ExpiresIn = 3600
#   )
#
#   return json.dumps({
#     'data': presigned_post,
#     'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
#   })