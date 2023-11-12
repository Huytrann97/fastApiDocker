import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

def analyse_document(endpoint, key, classifier_id, url):
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    print("-----------------------------------")
    print("----Classifying documents .... ----")
    print("-----------------------------------")
    poller = document_analysis_client.begin_classify_document(
       classifier_id, url
    )

    arrayResults =[]
    for doc in poller.result().documents:
        doc_result = {
            "type": doc.doc_type or "N/A",
            "confidence": doc.confidence
        }
        arrayResults.append(doc_result)
    print(arrayResults)
    return arrayResults

# Main code
