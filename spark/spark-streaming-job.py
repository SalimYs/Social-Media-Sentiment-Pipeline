
import os
import time
import logging
import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import from\_json, col, udf
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from dotenv import load\_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(**name**)
load\_dotenv()

bootstrap = os.getenv('KAFKA\_BOOTSTRAP\_SERVERS', 'kafka:9093')
topic = os.getenv('KAFKA\_TOPIC', 'social\_media\_posts')
spark\_master = os.getenv('SPARK\_MASTER', 'spark://spark-master:7077')
API = '[http://ml-api:5000/predict](http://ml-api:5000/predict)'

schema = StructType(\[
StructField('id', StringType()),
StructField('text', StringType()),
StructField('created\_at', TimestampType()),
StructField('keyword', StringType())
])

@udf(StringType())
def sentiment\_udf(text):
try:
r = requests.post(API, json={'text': text})
if r.ok:
return r.json().get('sentiment','neutral')
except:
pass
return 'neutral'

spark = SparkSession.builder.appName('Streaming').master(spark\_master).getOrCreate()
spark.sparkContext.setLogLevel('WARN')

df = spark.readStream.format('kafka')&#x20;
.option('kafka.bootstrap.servers', bootstrap)&#x20;
.option('subscribe', topic)&#x20;
.load()

parsed = df.selectExpr('CAST(value AS STRING)')&#x20;
.select(from\_json(col('value'), schema).alias('d')).select('d.\*')

out = parsed.withColumn('sentiment', sentiment\_udf(col('text')))

out.writeStream.format('memory').queryName('sentiments').outputMode('append').start()
out.writeStream.format('console').outputMode('append').start().awaitTermination()

