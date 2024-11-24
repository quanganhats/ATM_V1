import subprocess
import asyncio

async def mongoexp_archive(mongo_bin_path,host,port,username,password, db_name,db_collection, output_dir):
    try:
        command = [
        f"{mongo_bin_path}\mongodump",
        "--host", host,
        "--port", str(port),
        "-u", username,
        "-p", password,
        "--authenticationDatabase", "admin",
        "--db", db_name,
        '--collection', db_collection,
        "--dumpDbUsersAndRoles",
        "--gzip",
        "--out", output_dir
        ]
        subprocess.run(command)
        
    except Exception as e:
        print(f"Lỗi khi thực hiện mongodump: {e}")
        
async def mongoimp_archive(mongo_bin_path,host,port,username,password, db_name,db_collection, output_dir):
    try:
        command = [
        f"{mongo_bin_path}\mongorestore",
        "--host", host,
        "--port", str(port),
        "-u", username,
        "-p", password,
        "--authenticationDatabase", "admin",
        "--db", db_name,
        '--collection', db_collection,
        "--restoreDbUsersAndRoles",
        "--gzip",
        "--file", output_dir
        ]
        subprocess.run(command)
        
    except Exception as e:
        print(f"Lỗi khi thực hiện mongodump: {e}")




async def mongodump_archive(mongo_bin_path,host,port,username,password, db_name, output_dir):
    try:
        command = [
        f"{mongo_bin_path}\mongodump",
        "--host", host,
        "--port", str(port),
        "-u", username,
        "-p", password,
        "--authenticationDatabase", "admin",
        "--db", db_name,
        "--dumpDbUsersAndRoles",
        "--gzip",
        "--out", output_dir
        ]
        subprocess.run(command)
        
    except Exception as e:
        print(f"Lỗi khi thực hiện mongodump: {e}")
        
async def mongorestore_archive(mongo_bin_path,host,port,username,password, db_name, output_dir):
    try:
        command = [
        f"{mongo_bin_path}\mongorestore",
        "--host", host,
        "--port", str(port),
        "-u", username,
        "-p", password,
        "--authenticationDatabase", "admin",
        "--db", db_name,
        "--restoreDbUsersAndRoles",
        "--gzip",
        "--drop",
        "--dir", output_dir
        ]
        subprocess.run(command)
        
    except Exception as e:
        print(f"Lỗi khi thực hiện mongodump: {e}")



def exportX():
    try:
        asyncio.run(mongoexport_archive(r"D:\myfile.txt","test100","QueueTask"))
    except Exception as e:
        print(f"Lỗi khi thực hiện mongodump: {e}")
    
def importX():
    asyncio.run(mongoimport_archive(r"D:\myfile.txt","test100","QueueTask"))
    
def dumpX():
    mongo_bin_path=r"C:\Program Files\MongoDB\Server\4.0\bin"
    host = "localhost"
    port = 27017
    username = "a"
    password = "a"
    db_name = "DSADB"
    output_dir = r"D:\projects\DSA\Database\backup"
    try:
        asyncio.run(mongodump_archive(mongo_bin_path,host,port,username,password,db_name,output_dir))
        print(f"Mongodump thành công. Archive được lưu tại: {output_dir}")
    except Exception as e:
        print(f"Lỗi khi thực hiện mongodump: {e}")
        
def restoreX():
    mongo_bin_path=r"C:\Program Files\MongoDB\Server\4.0\bin"
    host = "localhost"
    port = 27017
    username = "a"
    password = "a"
    db_name = "DSADB"
    output_dir = r"D:\projects\DSA\Database\backup"
    try:
        asyncio.run(mongorestore_archive(mongo_bin_path,host,port,username,password,db_name,output_dir))
        print(f"Mongodump thành công. Archive được lưu tại: {output_dir}")
    except Exception as e:
        print(f"Lỗi khi thực hiện mongodump: {e}")

if __name__ == "__main__":
    dumpX()
    #restoreX()
    

    
# {
  # "_id": "DEMO_DMS.OADataServer",
  # "user": "OADataServer",
  # "db": "DEMO_DMS",
  # "credentials": {
    # "SCRAM-SHA-1": {
      # "iterationCount": {
        # "$numberInt": "10000"
      # },
      # "salt": "nFzVU9/w9ewLtlKvPIOG6A==",
      # "storedKey": "9d7lUCmn+kiOxN4Nkm8GMVjRFok=",
      # "serverKey": "4pKZaeFmKMC0LU4EOd5KnmUR//c="
    # },
    # "SCRAM-SHA-256": {
      # "iterationCount": {
        # "$numberInt": "15000"
      # },
      # "salt": "9NVsOTVJZBBRGxKrop0LHXvChSXPwaJL5Tagkg==",
      # "storedKey": "mbXG+DLWehA9LPIGerxohH8q5QiQh9F+y+PotdBqqTc=",
      # "serverKey": "w6Nx1eIYDZHHNYX5gnEhUJ/jjvXciV917eAeyJyLqNc="
    # }
  # },
  # "customData": {
    # "isBuiltinUser": true
  # },
  # "roles": [
    # {
      # "role": "readWrite",
      # "db": "DEMO_DMS"
    # }
  # ]
# }


# BackupModel collection000
# Simulation collection001
# Model collection002
# fs.chunks collection003
# Fep collection004
# Function collection005
# Config collection006
# Variable collection007
# FepLogs collection008
# Tagging collection009
# fs.files collection010
# Template collection011    
