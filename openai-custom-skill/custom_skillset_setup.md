# Set-up the OpenAI custom skillet

1. In the Azure Portal, get your Azure OpenAI key under the *Keys and Endpoint* section of the resource. Save it for later use.

2. In the [OpenAI studio](https://oai.azure.com/), access the playground, go to *Deployments* and create a new deployment with the model of your choice. Save the model name for later use.

3. Open the [open-ai-custom-skill](../openai-custom-skill) folder and open it in Visual Studio Code.

4. Run the `func init` command in the terminal. You will get a new configuration files *local.settings.json*.

5. Update *local.settings.json* with the following parameters:

   ```json
   { 
   	"IsEncrypted": false,
   
        "Values": {
   
           "FUNCTIONS_WORKER_RUNTIME": "python",
   
           "AzureWebJobsStorage": "UseDevelopmentStorage=true",
   
           "AZURE_OPENAI_SECRET": "[YOUR_AZURE_OPEN_AI_KEY]",
   
           "OPENAI_ENGINE": "[YOUR_OPEN-AI_MODEL]"
   
           }
   }
   ```

6. Update the [\_\_init\_\_.py](../openai-custom-skill/openai_request/__init__.py) function file by updating the global variables `OPENAI_ENDPOINT` and `OPENAI_PROMPT` with your Azure OpenAI endpoint and the prompt you would like to apply to the text of your documents.
7. Use the `func start` command in the command line to test locally. A local endpoint must appear at the end of the output.
8. Use this endpoint to make a `POST` Rest call with the following body format, which is the format of an [array of record](https://learn.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-interface#format-web-api-inputs) from Cognitive Search :

```json
{
    "values": [
      {
        "recordId": "0",
        "data": {
            "id": "1",
            "lang": "en",
            "text": "[SOME_TEST_TEXT]"
        }
      }
    ]
}
```

9. Deploy the function to Azure using `func azure functionapp publish <YOUR_FUNCTION_APP_NAME>`. Don't forget to copy the environment variables from *local.settings.json* to your application settings.
10. Save your function endpoint to use it in the Cognitive Search script.



If you are facing any issue, refer to the [Getting started with Azure Functions](../openai-custom-skill/getting_started_with_azure_functions.md) documentation.