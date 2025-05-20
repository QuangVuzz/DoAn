import streamlit as st
import random
from datetime import datetime
import pandas as pd
import io

st.set_page_config(
    page_title="Trợ Lý Mầm Non",
    page_icon="🧸", 
    layout="centered",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_csv_data():
    try:
        csv_data = """Thời gian,Hoạt động,Nhóm dưới 2 tuổi,Nhóm 3 – 4 tuổi,Nhóm 5 tuổi,
07:00 – 08:00,"Đón trẻ, chơi tự do",Chơi với đồ chơi mềm,"Xếp hình, đồ chơi phát triển vận động",Trò chơi phát triển tư duy,
08:00 – 08:30,Thể dục sáng,Vận động nhẹ,Bài thể dục vui nhộn,Thể dục bài bản theo nhạc,
08:30 – 09:00,Ăn sáng,"Cháo, sữa","Cơm nát, sữa","Cơm, món mặn, canh",
09:00 – 09:15,Vệ sinh cá nhân,"Lau mặt, thay tã","Tự rửa tay, vệ sinh cơ bản","Rửa mặt, đánh răng",
09:15 – 10:00,Hoạt động học theo chương trình,"Nhận biết màu sắc, hình khối","Làm quen chữ cái, số lượng nhỏ","Học chữ, số, chuẩn bị vào lớp 1",
10:00 – 10:30,Chơi ngoài trời,"Đi dạo, chơi cát",Chơi trò vận động nhóm,Trò chơi phát triển thể chất,
10:30 – 11:00,Hoạt động góc,"Xem tranh, chơi mềm","Xây dựng, gia đình, học tập","Phân vai, sáng tạo",
11:00 – 11:30,Ăn trưa,Cháo đặc,"Cơm nát, thức ăn mềm",Cơm bình thường,
11:30 – 14:00,Ngủ trưa,Ngủ có cô ru ngủ,Ngủ có nhạc nhẹ,Ngủ trưa tự lập,
14:00 – 14:30,Vệ sinh – Ăn xế,Ăn sữa chua/yogurt,"Bánh, sữa","Bánh ngọt, trái cây",
14:30 – 15:00,"Kể chuyện, âm nhạc","Nghe kể chuyện, ru ngủ nhẹ",Kể chuyện qua hình ảnh,"Nghe nhạc, kể chuyện nhóm",
15:00 – 16:00,Vui chơi tự do,"Chơi mềm, xe đẩy","Chơi xếp hình, vẽ màu",Trò chơi nhóm có luật,
16:00 – 17:00,Trả trẻ,"Cô trả trẻ, dặn dò","Dặn dò, chơi nhẹ","Dọn dẹp đồ dùng, chào ba mẹ",
,,,,,
,,,,,
Bữa ăn,Thứ Hai,Thứ Ba,Thứ Tư,Thứ Năm,Thứ Sáu
Bữa sáng,"Cháo thịt bằm, sữa tươi","Bún mọc, sữa đậu nành","Cháo cá hồi, sữa tươi","Mì gà rau củ, nước cam","Cháo gà bí đỏ, sữa tươi"
Bữa phụ sáng,"Trái cây (chuối, táo)",Sữa chua uống,"Bánh quy, nước lọc","Trái cây (đu đủ, lê)",Yaourt trái cây
Bữa trưa,"Cơm, cá kho, canh rau ngót, tráng miệng chuối","Cơm, gà xào nấm, canh cải xanh, tráng miệng táo","Cơm, thịt viên sốt cà, canh bí đỏ, thanh long","Cơm, trứng chiên thịt, canh rau dền, cam","Cơm, đậu hũ sốt cà, canh cải thảo, tráng miệng nho"
Bữa xế,"Bánh flan, sữa bột","Cháo đậu xanh, sữa bột","Xôi đậu phộng, nước lọc","Bánh mì sữa, sữa tươi","Nui nấu tôm, sữa chua"
Bữa phụ chiều,"Sữa tươi, bánh gạo","Sữa tươi, bánh mềm","Trái cây (cam, dưa hấu)","Sữa tươi, bánh quy","Sữa chua, trái cây tổng hợp"
"""
        
        lines = csv_data.strip().split('\n')
        
        empty_line_indices = [i for i, line in enumerate(lines) if line.strip() == ',,,,,']
        
        if empty_line_indices:
            schedule_data = '\n'.join(lines[:empty_line_indices[0]])
            schedule_df = pd.read_csv(io.StringIO(schedule_data))
            
            menu_start_idx = empty_line_indices[-1] + 2 
            menu_data = '\n'.join(lines[menu_start_idx:])
            menu_df = pd.read_csv(io.StringIO(menu_data))
            
            return {
                "Lịch hoạt động": schedule_df,
                "Thực đơn": menu_df
            }
        else:
            df = pd.read_csv(io.StringIO(csv_data))
            return {"Dữ liệu": df}
            
    except Exception as e:
        st.error(f"Lỗi khi xử lý dữ liệu CSV: {e}")
        return None

st.markdown("""
<style>
    .main-header {
        font-family: 'Comic Sans MS', cursive, sans-serif;
        color: #ff6b6b;
    }
    .stTextInput>div>div>input {
        border-radius: 20px;
    }
    .stButton>button {
        border-radius: 20px;
        background-color: #65b2ff;
        color: white;
        font-weight: bold;
    }
    .user-bubble {
        text-align: right;
        color: #155724;
        background-color: #d4edda;
        padding: 12px;
        border-radius: 18px 18px 0 18px;
        margin: 8px 0;
        display: inline-block;
        max-width: 80%;
        float: right;
        clear: both;
    }
    .bot-bubble {
        text-align: left;
        color: #0c5460;
        background-color: #cce5ff;
        padding: 12px;
        border-radius: 18px 18px 18px 0;
        margin: 8px 0;
        display: inline-block;
        max-width: 80%;
        float: left;
        clear: both;
    }
    .chat-container {
        overflow-y: auto;
        height: 400px;
        padding: 10px;
        display: flex;
        flex-direction: column;
    }
    .chat-wrapper {
        display: flex;
        flex-direction: column;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>🧸 Trợ Lý Trường Mầm Non Mầm Non Nhỏ</h1>", unsafe_allow_html=True)
st.markdown("Chào mừng phụ huynh! Tôi ở đây để giúp đỡ với mọi câu hỏi về lịch học, hoạt động, học tập và nhiều thông tin khác!")

csv_data = load_csv_data()

with st.sidebar:
    st.header("📋 Thông Tin Nhanh")
    st.info("**Giờ học**: 7:30 - 16:30 (Thứ 2 - Thứ 6)")
    st.info("**Địa chỉ**: 123 Đường Học Tập")
    st.info("**Điện thoại**: (028) 123-4567")
    
    if csv_data:
        st.header("📊 Dữ Liệu Có Sẵn")
        sheet_option = st.selectbox("Chọn Bảng:", options=list(csv_data.keys()))
        
        if sheet_option:
            df = csv_data[sheet_option]
            st.write(f"Xem trước dữ liệu {sheet_option}:")
            st.dataframe(df.head())
            
            csv_export = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Tải xuống dạng CSV",
                data=csv_export,
                file_name=f"{sheet_option}.csv",
                mime="text/csv",
            )
    else:
        st.warning("Không thể xử lý dữ liệu CSV. Vui lòng kiểm tra định dạng của tệp.")
    
    st.subheader("📝 Để lại tin nhắn cho nhân viên")
    parent_name = st.text_input("Tên phụ huynh")
    child_name = st.text_input("Tên học sinh")
    message = st.text_area("Tin nhắn")
    if st.button("Gửi Tin Nhắn"):
        if parent_name and child_name and message:
            st.success("Tin nhắn đã được gửi! Nhân viên sẽ liên hệ lại với bạn sớm.")
        else:
            st.error("Vui lòng điền đầy đủ tất cả các trường.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"sender": "bot", "text": "Xin chào! Tôi có thể giúp gì cho bạn hôm nay?"}
    ]

greetings = [
    "Xin chào! Tôi có thể giúp gì cho bạn hôm nay?",
    "Chào bạn! Tôi có thể giúp gì liên quan đến trường mầm non của con bạn?",
    "Xin chào! Tôi ở đây để trả lời các câu hỏi về trường mầm non.",
    "Chào mừng! Tôi có thể giúp gì về thông tin Trường Mầm Non Mầm Non Nhỏ?"
]

farewells = [
    "Tạm biệt! Chúc bạn một ngày tuyệt vời!",
    "Hẹn gặp lại! Đừng ngần ngại hỏi nếu bạn có thêm câu hỏi.",
    "Tạm biệt! Chúng tôi luôn sẵn sàng hỗ trợ.",
    "Tạm biệt nhé! Hãy liên hệ bất cứ lúc nào."
]

knowledge_base = {
    "schedule": [
        "Lịch hàng ngày của chúng tôi từ 7:30 đến 16:30, từ Thứ 2 đến Thứ 6. Có thể đưa trẻ đến sớm từ 7:00 với thỏa thuận trước.",
        "Đây là lịch trình điển hình hàng ngày của chúng tôi:\n• 7:30-8:30: Đến trường & Chơi tự do\n• 8:30-9:00: Vòng tròn buổi sáng\n• 9:00-10:00: Hoạt động học tập\n• 10:00-10:30: Giờ ăn nhẹ\n• 10:30-11:30: Chơi ngoài trời\n• 11:30-12:15: Ăn trưa\n• 12:15-13:30: Ngủ trưa/Thời gian yên tĩnh\n• 13:30-15:00: Nghệ thuật & Hoạt động\n• 15:00-15:30: Ăn nhẹ buổi chiều\n• 15:30-16:30: Chơi tự do & Đón về"
    ],
    "meals": [
        f"Thực đơn ăn trưa hôm nay gồm mì ống nguyên hạt với sốt rau, salad, và trái cây tươi. Đồ ăn nhẹ là bánh quy nguyên hạt với phô mai và táo cắt lát.",
        "Bữa ăn của chúng tôi tuân theo hướng dẫn dinh dưỡng cho trẻ mẫu giáo. Chúng tôi phục vụ bữa sáng, bữa trưa và hai bữa ăn nhẹ hàng ngày. Tất cả các bữa ăn đều không có đậu phộng và chúng tôi đáp ứng các hạn chế về chế độ ăn uống.",
        "Thực đơn tuần này bao gồm: Thứ 2 (Gà & cơm), Thứ 3 (Mì ống rau củ), Thứ 4 (Ngày bánh sandwich), Thứ 5 (Ngày bánh taco), và Thứ 6 (Ngày pizza). Trái cây và rau củ tươi được phục vụ với tất cả các bữa ăn."
    ],
    "activities": [
        "Trẻ em tham gia vào nhiều hoạt động giáo dục khác nhau bao gồm nghệ thuật & thủ công, âm nhạc, kể chuyện, xếp hình, đóng kịch, và khám phá ngoài trời.",
        "Các hoạt động đặc biệt tuần này bao gồm: Thứ 2 (Đi dạo thiên nhiên), Thứ 3 (Ngày Âm nhạc), Thứ 4 (Thí nghiệm Khoa học), Thứ 5 (Dự án Nghệ thuật), và Thứ 6 (Chia sẻ & Kể chuyện).",
        "Chúng tôi cân bằng giữa học tập có cấu trúc và thời gian chơi tự do. Các trung tâm hoạt động của chúng tôi bao gồm góc đọc sách, xếp hình, trạm nghệ thuật, khu vực đóng kịch, và trung tâm khám phá khoa học."
    ],
    "learning": [
        "Chương trình giảng dạy của chúng tôi tập trung vào phát triển cảm xúc xã hội, biết chữ sớm, khái niệm toán học, khám phá khoa học và phát triển thể chất phù hợp với độ tuổi mẫu giáo.",
        "Trẻ em học thông qua các hoạt động dựa trên trò chơi phát triển: tư duy phản biện, giải quyết vấn đề, kỹ năng giao tiếp, sáng tạo và kỹ năng xã hội.",
        "Chúng tôi tuân theo các mục tiêu học tập phù hợp với lứa tuổi bao gồm nhận biết chữ cái, đếm số, mẫu cơ bản, nhận dạng hình dạng và phát triển kỹ năng vận động tinh."
    ],
    "nap": [
        "Giờ ngủ trưa là từ 12:15 đến 13:30. Trẻ em nghỉ ngơi trên thảm cá nhân với chăn và đồ dùng thoải mái từ nhà.",
        "Mặc dù chúng tôi khuyến khích tất cả trẻ em nghỉ ngơi, những trẻ không ngủ có thể tham gia vào các hoạt động yên tĩnh sau 30 phút nghỉ ngơi.",
        "Vui lòng gửi một chiếc chăn nhỏ và đồ dùng thoải mái (nếu cần) cho giờ ngủ trưa. Tất cả các vật dụng nên được ghi nhãn tên của con bạn."
    ],
    "staff": [
        "Tất cả giáo viên của chúng tôi đều có bằng cấp và chứng chỉ giáo dục mầm non. Tỷ lệ học sinh-giáo viên là 8:1 để có sự chú ý tối ưu.",
        "Mỗi lớp học có một giáo viên chính và một trợ giảng. Nhân viên của chúng tôi tham gia đào tạo phát triển chuyên môn thường xuyên.",
        "Hiệu trưởng, cô Hương, đã làm việc tại Mầm Non Nhỏ trong 15 năm và giám sát tất cả các hoạt động lớp học và liên lạc với phụ huynh."
    ],
    "pickup": [
        "Giờ đón thông thường là từ 15:30 đến 16:30. Đón muộn có thể phát sinh phí bổ sung.",
        "Chỉ người lớn được ủy quyền có tên trong biểu mẫu đón của con bạn mới có thể đón trẻ. Vui lòng mang theo ID để xác minh.",
        "Nếu có người mới sẽ đón con bạn, vui lòng thông báo trước cho chúng tôi thông qua cổng thông tin phụ huynh hoặc gọi điện đến văn phòng."
    ],
    "illness": [
        "Trẻ em nên ở nhà nếu có sốt, nôn mửa, tiêu chảy hoặc tình trạng lây nhiễm. Các em nên không có triệu chứng trong 24 giờ trước khi quay lại.",
        "Nếu con bạn bị ốm ở trường, chúng tôi sẽ liên hệ ngay với bạn. Vui lòng đảm bảo thông tin liên hệ khẩn cấp của bạn được cập nhật.",
        "Để dùng thuốc, vui lòng điền vào các biểu mẫu cần thiết và cung cấp hướng dẫn của bác sĩ."
    ],
    "events": [
        "Các sự kiện sắp tới của chúng tôi bao gồm: Buổi họp Phụ huynh-Giáo viên (thứ Sáu tới), Lễ hội Mùa Thu (ngày 20 tháng 10), và Lễ Tạ ơn (ngày 22 tháng 11).",
        "Các đêm gắn kết gia đình hàng tháng được tổ chức vào thứ Năm cuối cùng của mỗi tháng từ 17:30 đến 19:00.",
        "Kiểm tra bản tin hàng tháng và cổng thông tin phụ huynh của chúng tôi để biết thông tin chi tiết về tất cả các sự kiện và hoạt động sắp tới."
    ],
    "supplies": [
        "Các vật dụng cần thiết bao gồm: quần áo dự phòng, bình nước, chăn ngủ trưa, tã/quần tập đi vệ sinh nếu cần, và quần áo ngoài trời phù hợp.",
        "Vui lòng ghi nhãn tất cả các vật dụng với tên của con bạn để tránh mất mát. Kiểm tra cập nhật vật dụng theo mùa của chúng tôi để biết các vật dụng bổ sung cần thiết.",
        "Vật dụng nghệ thuật và tài liệu học tập được cung cấp bởi trường. Không cần mang thêm tài liệu giáo dục."
    ]
}

def get_bot_response(message, csv_data=None):
    message = message.lower()
    
    def find_csv_info(keyword, csv_data):
        if not csv_data:
            return None
            
        results = []
        
        if "Lịch hoạt động" in csv_data:
            schedule_df = csv_data["Lịch hoạt động"]
            
            for index, row in schedule_df.iterrows():
                activity = str(row.get("Hoạt động", "")).lower()
                time_slot = str(row.get("Thời gian", "")).lower()
                
                if keyword in activity or keyword in time_slot:
                    age_groups = {
                        "nhỏ": "Nhóm dưới 2 tuổi",
                        "2 tuổi": "Nhóm dưới 2 tuổi", 
                        "3 tuổi": "Nhóm 3 – 4 tuổi",
                        "4 tuổi": "Nhóm 3 – 4 tuổi",
                        "5 tuổi": "Nhóm 5 tuổi"
                    }
                    
                    selected_age = "Nhóm 3 – 4 tuổi"  
                    
                    for age_keyword, age_column in age_groups.items():
                        if age_keyword in message:
                            selected_age = age_column
                            break
                    
                    results.append(f"• {row.get('Thời gian')}: {row.get('Hoạt động')} - {row.get(selected_age)}")
        
        if "Thực đơn" in csv_data:
            menu_df = csv_data["Thực đơn"]
            
            days = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu"]
            
            selected_day = None
            for day in days:
                day_lower = day.lower()
                if day_lower in message or day_lower.replace("thứ ", "t") in message:
                    selected_day = day
                    break
            
            meal_types = {
                "sáng": "Bữa sáng",
                "phụ sáng": "Bữa phụ sáng",
                "trưa": "Bữa trưa",
                "xế": "Bữa xế",
                "chiều": "Bữa phụ chiều"
            }
            
            selected_meal = None
            for meal_keyword, meal_name in meal_types.items():
                if meal_keyword in message:
                    selected_meal = meal_name
                    break
            
            for index, row in menu_df.iterrows():
                meal_type = str(row.get("Bữa ăn", "")).lower()
                
                if selected_meal and selected_meal.lower() in meal_type:
                    if selected_day:
                        results.append(f"• {row.get('Bữa ăn')} {selected_day}: {row.get(selected_day)}")
                    else:
                        meal_info = f"• {row.get('Bữa ăn')}: "
                        for day in days:
                            meal_info += f"\n  - {day}: {row.get(day)}"
                        results.append(meal_info)
                elif keyword in meal_type:
                    if selected_day:
                        results.append(f"• {row.get('Bữa ăn')} {selected_day}: {row.get(selected_day)}")
                    else:
                        meal_info = f"• {row.get('Bữa ăn')}: "
                        for day in days:
                            meal_info += f"\n  - {day}: {row.get(day)}"
                        results.append(meal_info)
        
        return results if results else None
    
    csv_keywords = {
        "lịch": ["lịch", "thời gian", "giờ", "ngày", "giờ học", "hoạt động"],
        "thực đơn": ["ăn", "thức ăn", "bữa", "món", "thực đơn", "dinh dưỡng", "đồ ăn"]
    }
    
    for category, keywords in csv_keywords.items():
        if any(keyword in message for keyword in keywords):
            if category == "lịch":
                schedule_info = find_csv_info("", csv_data)
                if schedule_info:
                    specific_schedule = [info for info in schedule_info if any(keyword in info.lower() for keyword in keywords)]
                    if specific_schedule:
                        return "Dựa trên lịch trình của chúng tôi:\n" + "\n".join(specific_schedule)
            elif category == "thực đơn":
                menu_info = find_csv_info("", csv_data)
                if menu_info:
                    specific_menu = [info for info in menu_info if any(keyword in info.lower() for keyword in keywords)]
                    if specific_menu:
                        return "Đây là thông tin về thực đơn:\n" + "\n".join(specific_menu)
    
    if any(word in message for word in ["xin chào", "chào", "hi", "hello"]):
        return random.choice(greetings)
    
    elif any(word in message for word in ["tạm biệt", "bye", "hẹn gặp lại"]):
        return random.choice(farewells)
    
    elif any(word in message for word in ["lịch", "thời khóa biểu", "hoạt động"]):
        return random.choice(knowledge_base["schedule"])
    
    elif any(word in message for word in ["ăn", "thức ăn", "bữa", "thực đơn"]):
        return random.choice(knowledge_base["meals"])
    
    elif any(word in message for word in ["chơi", "hoạt động", "vui chơi"]):
        return random.choice(knowledge_base["activities"])
    
    elif any(word in message for word in ["học", "học tập", "dạy", "giáo dục"]):
        return random.choice(knowledge_base["learning"])
    
    elif any(word in message for word in ["ngủ trưa", "nghỉ trưa", "ngủ", "nghỉ ngơi"]):
        return random.choice(knowledge_base["nap"])
    
    elif any(word in message for word in ["giáo viên", "nhân viên", "cô giáo", "thầy giáo"]):
        return random.choice(knowledge_base["staff"])
    
    elif any(word in message for word in ["đón", "đưa", "đón con"]):
        return random.choice(knowledge_base["pickup"])
    
    elif any(word in message for word in ["bệnh", "ốm", "thuốc", "sức khỏe"]):
        return random.choice(knowledge_base["illness"])
    
    elif any(word in message for word in ["sự kiện", "lễ hội", "họp phụ huynh"]):
        return random.choice(knowledge_base["events"])
    
    elif any(word in message for word in ["đồ dùng", "vật dụng", "quần áo", "mang theo"]):
        return random.choice(knowledge_base["supplies"])
    
    else:
        return "Xin lỗi, tôi không hiểu câu hỏi của bạn. Bạn có thể hỏi về lịch học, thực đơn, hoạt động hàng ngày, hoặc các thông tin khác về trường mầm non không?"

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
st.markdown("<div class='chat-wrapper'>", unsafe_allow_html=True)

for message in st.session_state.messages:
    if message["sender"] == "user":
        st.markdown(f"<div class='user-bubble'>{message['text']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-bubble'>{message['text']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

with st.form(key="chat_form", clear_on_submit=True):
    cols = st.columns([4, 1])
    with cols[0]:
        user_input = st.text_input("Nhập câu hỏi của bạn:", key="user_input")
    with cols[1]:
        submit_button = st.form_submit_button("Gửi")

    if submit_button and user_input:
        st.session_state.messages.append({"sender": "user", "text": user_input})
        
        response = get_bot_response(user_input, csv_data)
        
        st.session_state.messages.append({"sender": "bot", "text": response})
        
        st.rerun()

st.markdown("---")
st.markdown("© 2023 Trường Mầm Non Mầm Non Nhỏ. Liên hệ: mamnonnho@email.vn")