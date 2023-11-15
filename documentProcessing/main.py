import os
import time

# from azureTrain.classifyDocument import checkWhichDocument
from .classifyDocument import analyse_document
from .extractText import extract_text
from .extractPassport import extract_passport

# -----------set value here------------#

url = "https://scontent.fdad2-1.fna.fbcdn.net/v/t1.15752-9/373483333_720806080085391_8759204674535948605_n.png?_nc_cat=101&ccb=1-7&_nc_sid=8cd0a2&_nc_ohc=S20DrnQ3xpwAX8ixdNr&_nc_ht=scontent.fdad2-1.fna&oh=03_AdSRvrpeDhzhpC_q76x1nscHL5olKYAcGu37h_ukfecoEg&oe=65759087"


def process_document(url):
    key = ""
    endpoint = "https://eastus.api.cognitive.microsoft.com/"
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

    # -----------main logic------------#
    start_time = time.time()

    document = analyse_document(endpoint, key, "anaylyse_document", url)
    documentType = document[0]["type"]
    documentConfidence = document[0]["confidence"]

    if documentConfidence >= 0.5:
        print("Document type: ", documentType, "  confidence", documentConfidence)
        print("\nExtracting text  ")
        match documentType:
            case "lisense":
                return extract_text(key, endpoint, url, "lisence")
            case "my_number":
                return extract_text(key, endpoint, url, "my_number")
            case "residence_card":
                return extract_text(key, endpoint, url, "residence_card")
            case "passport":
                return extract_passport(key, endpoint, url)

            case other:
                print("please try other image ")

    else:
        print("Document not found, please try other image")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken to execute: {elapsed_time:.2f} seconds")


# --------------------------------------#

if __name__ == "__main__":
    process_document(url)

# -------------------------------#
