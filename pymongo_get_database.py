from pymongo import MongoClient
def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb://192.168.1.166:27017/intranet"
 
   # Cree una conexión con MongoClient. Puede importar MongoClient o usar pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Cree la base de datos para nuestro ejemplo (usaremos la misma base de datos en todo el tutorial
   return client['intranet']
  
# Esto se agrega para que muchos archivos pueden reutilizar la función get_database()
if __name__ == "__main__":   
   dbname = get_database()





