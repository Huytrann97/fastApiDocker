from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from .uploadS3 import get_s3_image_url

from database import SessionLocal
import models

def extract_text(key, endpoint, url, model_id, imageName):
    # Khởi tạo client
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    # Bắt đầu phân tích tài liệu
    poller = document_analysis_client.begin_analyze_document(model_id, url)
    result = poller.result()

    result_dict = {}
    # Trích xuất thông tin từ tài liệu
    for idx, document in enumerate(result.documents):
        print("--------Analyzing document #{}--------\n".format(idx + 1))
        for name, field in document.fields.items():
            field_value = field.value if field.value else field.content
            # Lưu giữ cặp khóa-giá trị vào từ điển
            result_dict[name] = field_value

    s3_url= get_s3_image_url(imageName)
    print("s3url is",s3_url)
    # add to database
    db = SessionLocal()
    try:
         # add card information to database
        new_card = models.Card()
        new_card.front_image_url= s3_url
        
        # add profile information to database
        new_user = models.User()
        new_user.card_id=result_dict["Id number"]
        new_user.full_name=result_dict["Last Name"]+" "+result_dict["Firstname"]
        new_user.birthday=result_dict["Date of Birth"]
        new_user.address=result_dict["Address"]
        new_user.expire_date=result_dict["Date valid"]
        
        db.add(new_card)
        db.add(new_user)
        db.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        db.close()

    return result_dict


# Test the function
