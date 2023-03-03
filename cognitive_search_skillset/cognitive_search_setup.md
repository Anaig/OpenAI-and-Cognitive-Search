# Set-up the new skill in the Azure Cognitive Search indexer

In this example, we will use the REST APIs to deploy the Azure Cognitive Search indexer.

- [x] **If you have an existing indexer:** You can add the new skills using the steps below.
- [ ] **If you don't have an indexer yet:** You can use the [Postman collection](../Cognitive Search-OpenAI Integration.postman_collection.json) in this repository as a deployment template, after updating the parameters in the [ Postman environment](../Cognitive Search-OpenAI Integration.postman_environment.json) file.

## Skillset

In the [Cognitive Search skillset](https://learn.microsoft.com/en-us/rest/api/searchservice/create-skillset#request-body), add a skill as the example below.

- If your text is is longer than the number of tokens supported by OpenAI, you can use `"/document/pages/*"` as a context and source to apply the OpenAI prompt at the page level.

- Replace `uri` with your Azure Functions endpoint, in the format *https://YOUR_WEB_APP_NAME.azurewebsites.net/api/FUNCTION_NAME*.

- Replace `"x-functions-key"` with your Azure Functions secret. You can find it under the *App Keys* section in the Azure portal.

```  json
    {
        "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
        "name": "summary-custom-skill",
        "description": "Short summary OpenAI generated",
        "context": "/document/merged_text",
        "uri": "[YOUR_AZURE_FUNCTIONS_ENDPOINT]",
        "httpMethod": "POST",
        "timeout": "PT30S",
        "batchSize": 1,
        "degreeOfParallelism": 1,
        "inputs": [
          {
            "name": "text",
            "source": "/document/merged_text"
          }
        ],
        "outputs": [
          {
            "name": "summary",
            "targetName": "summary"
          }
        ],
        "httpHeaders": {
          "x-functions-key": "[YOUR_AZURE_FUNCTIONS_KEY]"
        }
      }
```

## Index

Add a new field in the [index](https://learn.microsoft.com/en-us/rest/api/searchservice/create-index#request-body) for the custom skill.

```  json
    {
      "name": "summary",
      "type": "Edm.String",
      "searchable": true,
      "sortable": false,
      "filterable": false,
      "facetable": false
    }
```

## Indexer

Add a new output field mapping in the [indexer](https://learn.microsoft.com/en-us/rest/api/searchservice/create-indexer#request-body).

```    json
{
  "sourceFieldName": "/document/merged_text",
  "targetFieldName": "summary"
}
```

