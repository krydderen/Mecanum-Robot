# import libs
import uvicorn
from vidgear.gears.asyncio import WebGear

# initialize WebGear app  
web=WebGear(source=0)

# run this app on Uvicorn server
uvicorn.run(web(), host='192.168.1.241', port=8000)

# close app safely
web.shutdown()