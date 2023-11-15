from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient


def extract_text(key, endpoint, url, model_id):
    # Khởi tạo client
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    # Bắt đầu phân tích tài liệu
    poller = document_analysis_client.begin_analyze_document(model_id, url)
    result = poller.result()

    result_array = []
    # In thông tin trích xuất từ tài liệu
    for idx, document in enumerate(result.documents):
        print("--------Analyzing document #{}--------\n".format(idx + 1))
        for name, field in document.fields.items():
            field_value = field.value if field.value else field.content
            print("'{}': '{}' ".format(name, field_value, field.confidence))
            result_array.append(
                "'{}': '{}'".format(name, field_value, field.confidence)
            )
    return result_array


# Test the function
