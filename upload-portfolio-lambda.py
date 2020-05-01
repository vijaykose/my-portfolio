import boto3
from io import BytesIO
import zipfile
import mimetypes

def lambda_handler(event, context):
    s3 = boto3.resource('s3')

    portfolio_bucket = s3.Bucket('vijaykoseportfolio')
    build_bucket = s3.Bucket('vijaykoseportfoliobuild')

    portfolio_zip = BytesIO()
    build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)

    with zipfile.ZipFile(portfolio_zip) as myzip:
        for nm in myzip.namelist():
            obj = myzip.open(nm)
            portfolio_bucket.upload_fileobj(obj, nm)
            portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

    print ("Job done!")

    return ('Hello from Lambda!')
