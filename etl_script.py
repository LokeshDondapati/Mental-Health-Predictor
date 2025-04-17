import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import col, lower, trim, when
from awsglue.dynamicframe import DynamicFrame

# Initialize contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Parameters (optional if you're using job arguments)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Read from Glue Catalog table
raw_dyf = glueContext.create_dynamic_frame.from_catalog(
    database="mental_health_db",
    table_name="mental_health_dataset_capstone"
)

# Convert to Spark DataFrame for transformation
df = raw_dyf.toDF()

# Rename columns to snake_case
for colname in df.columns:
    df = df.withColumnRenamed(colname, colname.lower().replace(" ", "_"))

# Standardize gender column
df = df.withColumn("gender", lower(trim(col("gender"))))
df = df.withColumn("gender", when(col("gender").isin("male", "m"), "Male")
                   .when(col("gender").isin("female", "f"), "Female")
                   .otherwise("Other"))

# (Optional) Drop any nulls in important columns
df = df.dropna(subset=["user_id", "age"])

# Convert back to DynamicFrame for Glue write
cleaned_dyf = DynamicFrame.fromDF(df, glueContext, "cleaned_dyf")

# Write cleaned data to processed S3 bucket in Parquet format
glueContext.write_dynamic_frame.from_options(
    frame=cleaned_dyf,
    connection_type="s3",
    connection_options={
        "path": "s3://mental-health-dataset-capstone/processed/mental_health_cleaned/",
        "partitionKeys": []  # You can add partitioning by 'country' or 'gender' if needed
    },
    format="parquet"
)
