# run from repository root

export PYTHONUNBUFFERED=1
export FLASK_APP=dtool_lookup_server
export JWT_PUBLIC_KEY_FILE=$(pwd)/keys/jwt.pub
export JWT_PRIVATE_KEY_FILE=$(pwd)/keys/jwt

openssl genrsa -out ${JWT_PRIVATE_KEY_FILE} 2048
openssl rsa -in ${JWT_PRIVATE_KEY_FILE} -pubout -outform PEM -out ${JWT_PUBLIC_KEY_FILE}

docker run -d -p 27017:27017 -v $(pwd)/data:/data/db mongo

flask db init
flask db migrate
flask db upgrade

flask base_uri add s3://test-bucket
flask base_uri add smb://test-share

flask base_uri index s3://test-bucket
flask base_uri index smb://test-share

flask user add testuser
flask user search_permission testuser s3://test-bucket
flask user register_permission testuser s3://test-bucket

flask run

# run after server is up
# flask user token testuser
