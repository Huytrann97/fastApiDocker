from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

def extract_text(key, endpoint, url, model_id):
    # Khởi tạo client
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    # Bắt đầu phân tích tài liệu
    poller = document_analysis_client.begin_analyze_document_from_url(
        model_id, url)
    result = poller.result()
    return result

# Test the function
def print_result(result):
    print("--------Printing results--------\n")
    for idx, document in enumerate(result.documents):
        for name, field in document.fields.items():
            field_value = field.value if field.value else field.content
            print("'{}': '{}' ".format(
                name, field_value, field.confidence))
