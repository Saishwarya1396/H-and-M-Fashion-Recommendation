import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, sum as spark_sum

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

#jdbc Hritik's pc

customers_df = spark.read.format("jdbc").option("url", "jdbc:mysql://project-h-and-m-db.ciuejmixu9um.us-east-1.rds.amazonaws.com:3306/project_h_and_m_db").option("dbtable", "customers").option("user", "admin").option("password", "12345678").load() 

articles_df = spark.read.format("jdbc").option("url", "jdbc:mysql://project-h-and-m-db.ciuejmixu9um.us-east-1.rds.amazonaws.com:3306/project_h_and_m_db").option("dbtable", "articles").option("user", "admin").option("password", "12345678").load() 

transaction_df = spark.read.format("jdbc").option("url", "jdbc:mysql://project-h-and-m-db.ciuejmixu9um.us-east-1.rds.amazonaws.com:3306/project_h_and_m_db").option("dbtable", "transactions").option("user", "admin").option("password", "12345678").load() 

#own bucket
customers_df.repartition(1).write.mode('overwrite').parquet("s3://data-lake-h-m-as-5/Customers/Customers_Live/")

articles_df.repartition(1).write.mode('overwrite').parquet("s3://data-lake-h-m-as-5/Articles/Articles_Live/")

transaction_df.repartition(1).write.mode('append').parquet("s3://data-lake-h-m-as-5/Transactions/Transactions_Live/")


job.commit()