from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient


def extract_passport(key, endpoint, url):
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_analysis_client.begin_analyze_document("prebuilt-idDocument", url)
    id_documents = poller.result()
    document = id_documents.documents[0]

    result_list = []

    # if  document.fields['MachineReadableZone'].value != None:
    if "MachineReadableZone" in document.fields:
        print(" Text from machine readable zone: \n")
        machine_readable_texts = document.fields["MachineReadableZone"].value
        # Trích xuất dữ liệu
        extracted_data = {
            key: field.value for key, field in machine_readable_texts.items()
        }
        # In thông tin đã trích xuất
        for key, value in extracted_data.items():
            print(f"{key}: {value}")
            result_list.append({key: value})

    else:
        print("cannot extract data")
        return "cannot extract data"

    return result_list

    # print("\n Text from fields: \n")
    # place_of_birth = document.fields['PlaceOfBirth'].value
    # type = document.fields['DocumentType'].value
    # date_issue = document.fields['DateOfIssue'].value

    # print(f"Place of birth: {place_of_birth}")
    # print(f"Document type: {type}")
    # print(f"Date of issue: {date_issue}")
