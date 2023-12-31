import os
import time

# from azureTrain.classifyDocument import checkWhichDocument
from .classifyDocument import analyse_document
from .extractTextByImage import extract_text
from .extractPassport import extract_passport

from .utils import delete_image

from PIL import Image
import io
from dotenv import load_dotenv

from sqlalchemy.orm import Session


load_dotenv()

# -----------set value here------------#

# url = "https://scontent.fdad2-1.fna.fbcdn.net/v/t1.15752-9/373483333_720806080085391_8759204674535948605_n.png?_nc_cat=101&ccb=1-7&_nc_sid=8cd0a2&_nc_ohc=S20DrnQ3xpwAX8ixdNr&_nc_ht=scontent.fdad2-1.fna&oh=03_AdSRvrpeDhzhpC_q76x1nscHL5olKYAcGu37h_ukfecoEg&oe=65759087"

# image_path = "image1.jpg"
# with open(image_path, "rb") as image_file:
#     url = image_file.read()


def process_document(imageName):
    AZURE_KEY = os.getenv("AZURE_KEY")
    AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
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
            endpoint=AZURE_ENDPOINT, credential=AzureKeyCredential(AZURE_KEY)
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

    # ---------------note here: url is image file
    image_path = "processing_image/" + imageName
    with open(image_path, "rb") as image_file:
        url = image_file.read()
    # ----------------------

    document = analyse_document(AZURE_ENDPOINT, AZURE_KEY, "model202311172", url)
    documentType = document[0]["type"]
    documentConfidence = document[0]["confidence"]

    reesponse = ""

    if documentConfidence >= 0.3:
        print("Document type: ", documentType, "  confidence", documentConfidence)
        print("\nExtracting text  ")
        match documentType:
            case "lisense":
                reesponse = extract_text(AZURE_KEY, AZURE_ENDPOINT, url, "lisence", imageName)
            case "my_number":
                reesponse = extract_text(AZURE_KEY, AZURE_ENDPOINT, url, "my_number", imageName)
            case "residence_card":
                reesponse = extract_text(
                    AZURE_KEY, AZURE_ENDPOINT, url, "residence_card", imageName
                )
            case "passport":
                reesponse = extract_passport(AZURE_KEY, AZURE_ENDPOINT, url)
            case "Vietnamese_idcard":
                reesponse = extract_text(
                    AZURE_KEY, AZURE_ENDPOINT, url, "VietnameseIdCard",imageName
                )

            case other:
                print("please try other image ")
                reesponse = "please try other image "

    else:
        print("Document not found, please try other image")
        reesponse = "Document not found, please try other image"

    delete_image(imageName)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken to execute: {elapsed_time:.2f} seconds")

    return reesponse


# --------------------------------------#

if __name__ == "__main__":
    process_document("url")

# -------------------------------#
