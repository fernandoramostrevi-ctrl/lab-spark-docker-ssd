from pyspark.sql import SparkSession

# Conectar a Spark Master
spark = SparkSession.builder \
    .appName('Test Conexion Spark') \
    .master('spark://localhost:7077') \
    .getOrCreate()

print('✅ Conexión exitosa a Spark')
print(f'Versión Spark: {spark.version}')
print(f'Master URL: {spark.sparkContext.master}')

spark.stop()
