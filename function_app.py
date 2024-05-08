import azure.functions as func
import logging
import json
from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient

app = func.FunctionApp()

credential = DefaultAzureCredential()
client = CosmosClient(url="https://thetrustedtap.documents.azure.com:443/", credential=credential)

@app.function_name(name="getEstablishments")
@app.route(route="getEstablishments", auth_level=func.AuthLevel.ANONYMOUS)
def get_establishments(req: func.HttpRequest) -> func.HttpResponse:
    try:
        database_name = "prod"  
        container_name = "establishment"
        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)

        query = "SELECT * FROM c"  
        results = container.query_items(query=query, enable_cross_partition_query=True)

        establishments = [result for result in results]

        return func.HttpResponse(
            json.dumps(establishments),
            mimetype="application/json",
            status_code=200,
            headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
            }
        )

    except Exception as e:
        logging.error(f"Cosmos DB error: {str(e)}")
        return func.HttpResponse(f"Error retrieving establishments: {str(e)}", status_code=500)
    
@app.function_name(name="HttpTrigger1")
@app.route(route="ping", auth_level=func.AuthLevel.ANONYMOUS)
def ping(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Ping received.')

    if req.method == 'OPTIONS':
        # Handle preflight requests (important for CORS)
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return func.HttpResponse('', status_code=204, headers=headers)
    
    if req.method == 'POST':
        headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
        }
        return func.HttpResponse("Pong", status_code=200, headers=headers)

    else: 
        return func.HttpResponse("HTTP trigger function processed a request, but the method is not allowed.", status_code=405) 
