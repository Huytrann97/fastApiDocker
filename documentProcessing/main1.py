import os
import time

# from azureTrain.classifyDocument import checkWhichDocument
from classifyDocument import analyse_document
from extractText1 import extract_text, print_result
from extractPassport import extract_passport
from concurrent.futures import ThreadPoolExecutor
#-----------set value here------------#
print()
key = ""
endpoint = "https://eastus.api.cognitive.microsoft.com/"
url = "https://scontent.fdad2-1.fna.fbcdn.net/v/t1.15752-9/373483333_720806080085391_8759204674535948605_n.png?_nc_cat=101&ccb=1-7&_nc_sid=8cd0a2&_nc_ohc=S20DrnQ3xpwAX8ixdNr&_nc_ht=scontent.fdad2-1.fna&oh=03_AdSRvrpeDhzhpC_q76x1nscHL5olKYAcGu37h_ukfecoEg&oe=65759087"
#--------------------------------------#

if __name__ == "__main__":
    from azure.core.exceptions import HttpResponseError

    try:
        start_timee = time.time()
        classifier_id = None
        if os.getenv("CLASSIFIER_CONTAINER_SAS_URL") and not os.getenv("CLASSIFIER_ID"):
            from azure.core.credentials import AzureKeyCredential
            from azure.ai.formrecognizer import (
                DocumentModelAdministrationClient,
                ClassifierDocumentTypeDetails,
                BlobSource,
            )

            endpoint = os.environ["AZURE_FORM_RECOGNIZER_ENDPOINT"]
            key = os.environ["AZURE_FORM_RECOGNIZER_KEY"]
            blob_container_sas_url = os.environ["CLASSIFIER_CONTAINER_SAS_URL"]

            document_model_admin_client = DocumentModelAdministrationClient(
                endpoint=endpoint, credential=AzureKeyCredential(key)
            )

            poller = document_model_admin_client.begin_build_document_classifier(
                doc_types={
                    "IRS-1040-A": ClassifierDocumentTypeDetails(
                        source=BlobSource(
                            container_url=blob_container_sas_url,
                            prefix="IRS-1040-A/train",
                        )
                    ),
                    "IRS-1040-D": ClassifierDocumentTypeDetails(
                        source=BlobSource(
                            container_url=blob_container_sas_url,
                            prefix="IRS-1040-D/train",
                        )
                    ),
                }
            )
            classifier = poller.result()
            classifier_id = classifier.classifier_id
        end_timee = time.time()
        elapsed_timee = end_timee - start_timee
        print(f"Time to call 1 : {elapsed_timee:.2f} seconds")

#-----------main logic------------#
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=2) as executor:
            future1 = executor.submit(analyse_document, endpoint, key, "anaylyse_document", url)
            future2 = executor.submit(extract_text, key, endpoint, url, "residence_card")

            document = future1.result()
            print(document)
            documentType = document[0]["type"]
            print(documentType)
            documentConfidence = document[0]["confidence"]
            print(documentConfidence)

        if documentConfidence >= 0.5:
            print("Document type: ", documentType,"  confidence", documentConfidence)
            match documentType:
                # case "lisense":
                #     extract_text(key, endpoint, url, "lisence")
                # case "my_number":
                #     extract_text(key, endpoint, url, "my_number")
                case "residence_card":
                    print("\n" ,print_result(future2.result()))
                # case "passport":
                #     extract_passport(key, endpoint, url)
                
                case other:
                    print("please try other image ")

        else:
            print("Document not found, please try other image")
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken to execute: {elapsed_time:.2f} seconds")
#-------------------------------#

    except HttpResponseError as error:
        print(
            "For more information about troubleshooting errors, see the following guide: "
            "https://aka.ms/azsdk/python/formrecognizer/troubleshooting"
        )
        # Examples of how to check an HttpResponseError
        # Check by error code:
        if error.error is not None:
            if error.error.code == "InvalidImage":
                print(f"Received an invalid image error: {error.error}")
            if error.error.code == "InvalidRequest":
                print(f"Received an invalid request error: {error.error}")
            # Raise the error again after printing it
            raise
        # If the inner error is None and then it is possible to check the message to get more information:
        if "Invalid request".casefold() in error.message.casefold():
            print(f"Uh-oh! Seems there was an invalid request: {error}")
        # Raise the error again
        raise
