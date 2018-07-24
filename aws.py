#Shangeetha Ravichandran
from flask import Flask, request, render_template, redirect, url_for,make_response
import boto3
from boto3.session import Session
import os

app = Flask(__name__)
session = Session(aws_access_key_id='####',
                  aws_secret_access_key='P####',
                  region_name='us-west-2')

# Create buckets
session1 = session.resource('s3')
s3 = boto3.resource('s3')


# s3.create_bucket(Bucket='mybucket')
# s3.create_bucket(Bucket='mybucket', CreateBucketConfiguration={
# 'LocationConstraint': 'us-west-2'})

@app.route('/', methods=['POST', 'GET'])
def login():
    obj = s3.Object(bucket_name='sangbucket', key='login.txt')
    users = obj.get()["Body"].read()
    user_name = request.form['user_name']
    flag1 = 0
    for data in users.splitlines():
        if (data == user_name):
            flag1 = 1
        if (flag1 == 0):
            return redirect(url_for('login'))
        else:
            print "Login scuccessful"
    return render_template('index.html')
        


@app.route('/upload', methods=['POST'])
def file_upload():
    file = request.files['upload_file']
    content = file.read()
    file_name = str(file)
    session1.Bucket('sangbucket').put_object(Key=file_name, Body=content)
    return render_template('upload.html')


@app.route("/download", methods=["POST"])
def file_downlaod():
    file = request.form['download_file']
    s3 = boto3.resource('s3', aws_access_key_id='####',
                        aws_secret_access_key='####')
    file_name = s3.Object('sangbucket', file)
    file_content = file_name.get()['Body'].read()
    response = make_response(file_content)
    response.headers["Content-Disposition"] = "attachment; filename=" + file
    return response
    return render_template('download.html')


# delete
@app.route("/delete", methods=["POST"])
def delete_files():
    file = request.form['delete_file']
    s3 = boto3.resource('s3', aws_access_key_id='####',
                        aws_secret_access_key='####')
    s3.Object('sangbucket', file).delete()
    return render_template('Delete.html')


if __name__ == '__main__':
    app.debug = 'true'
    app.run()
