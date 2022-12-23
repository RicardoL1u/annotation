CONTAINER_ID='a9a4b45f5a57'
docker export --output "${CONTAINER_ID}.tar" $CONTAINER_ID
tar -xf "${CONTAINER_ID}.tar" -C temp/

mkdir instance/last_version
mv instance/database.db instance/last_version/
cp temp/app/instance/database.db instance/database.db
cp temp/app/instance/database.db instance/"${CONTAINER_ID}.db"

mkdir data/last_version
mv data/*.json data/last_version
mkdir data/$CONTAINER_ID
cp temp/app/data/*.json data/$CONTAINER_ID/
cp temp/app/data/*.json data/
rm -rf temp/*