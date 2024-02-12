import azure.functions as func
import openai
import os
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Assuming the audio file is uploaded directly in the request body.
        # For larger files, consider using Azure Blob Storage and passing a URL instead.
        audio_file = req.get_body()

        # api_key = os.environ.get('mkh_openai_apikey')

        # Initialize OpenAI client
        client = openai.OpenAI(api_key=api_key)

        # For demonstration, directly using the audio file from the request.
        # In practice, you might save this to a temp file or blob storage first.
        transcript_response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        transcript = transcript_response['data']['text']  # Adjust based on the actual response structure

        # Assuming the same API key works for GPT-3. Adjust as necessary.
        chat_response = client.chat.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Summarize the following transcript."},
                      {"role": "user", "content": transcript}]
        )
        summary = chat_response.choices[0].message.content

        # Constructing response
        response_message = json.dumps({
            "transcript": transcript,
            "summary": summary
        })

        return func.HttpResponse(response_message, mimetype="application/json")
    except Exception as e:
        return func.HttpResponse(f"Error processing request: {str(e)}", status_code=500)