
import os
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import count, when, col
from dotenv import load\_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
load\_dotenv()

spark = SparkSession.builder.appName('Batch').master(os.getenv('SPARK\_MASTER')).getOrCreate()

df = spark.sql('SELECT \* FROM sentiments')
summary = df.groupBy('keyword').agg(
count('\*').alias('total'),
count(when(col('sentiment')=='positive',True)).alias('pos'),
count(when(col('sentiment')=='negative',True)).alias('neg'),
count(when(col('sentiment')=='neutral',True)).alias('neu')
).withColumn('pos\_pct',col('pos')\*100/col('total'))

summary.show()
summary.write.mode('overwrite').saveAsTable('sentiment\_summary')
