import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Parse the number from the query string
        number_str = req.params.get('number')
        if not number_str:
            try:
                req_body = req.get_json()
                number_str = req_body.get('number')
            except ValueError:
                pass
        
        if not number_str:
            return func.HttpResponse(
                "Please pass a number on the query string or in the request body",
                status_code=400
            )

        # Multiply the number by 2
        number = int(number_str)
        result = number * 2

        # Return the result
        return func.HttpResponse(json.dumps({"result": result}), mimetype="application/json")
    except Exception as e:
        return func.HttpResponse(f"Error processing request: {str(e)}", status_code=500)