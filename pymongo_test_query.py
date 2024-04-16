# Obtener la base de datos usando el método que definimos
from pymongo_get_database import get_database
dbname = get_database()
 
# Recuperar una colección llamada "user_1_items" de la base de datos
cabeot = dbname["cabeot"]
 
pipeline = [
    {"$project":{"_id":0,}},
    {"$match": {"c_numot": 1000028211}},  
    {
        "$lookup": {
            "from": 'detaot',
            "localField": 'c_numot',
            "foreignField": 'c_numot',
            "as": 'DetalleOt',
            "pipeline": [
                {"$project":{"_id":0}} ,
                {
                    "$lookup": {
                        "from": 'notmae',
                        "localField": 'c_numot',
                        "foreignField": 'c_NumOT',
                        "as": 'NotaSalida',
                        "pipeline": [
                            {"$project":{"_id":0}} ,
                            {
                                "$lookup": {
                                    "from": 'notmov',
                                    "localField": 'NT_NDOC',
                                    "foreignField": 'NT_NDOC',
                                    "as": 'NotaSalidaDetalle',
                                    "pipeline": [
                                        {"$project":{"_id":0}},
                                        {
                                            "$lookup": {
                                                "from": 'invmae',
                                                "localField": 'NT_CART',
                                                "foreignField": 'IN_CODI',
                                                "as": 'DetalleInsumo',
                                                "pipeline": [
                                                    {"$project":{"_id":0,"IN_ARTI":1,"IN_UVTA":1,"IN_COST":1}},                       
                                                ]
                                            }
                                        }
                                    ]
                                }
                            }
                        ],    
                    },
                }
            ]
        }
    },   

]

item_details = cabeot.aggregate(pipeline)
#item_details = cabeot.find().limit(1)
print("olitas")
#print(item_details[0]->c_desequipo)
for item in  item_details:
 # Esto no proporciona una salida muy legible
  print("dentro")
  print(item)