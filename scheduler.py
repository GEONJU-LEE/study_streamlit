import streamlit as st
from datetime import datetime
import uuid

# 전역 변수로 미팅 정보를 저장할 딕셔너리 (실제 앱에서는 DB를 사용하는 것이 적합)
meetings = {}

# 1. 첫 화면 구현
def main():
    st.title("미팅 스케줄러")

    option = st.selectbox("원하는 작업을 선택하세요", ["미팅 잡기", "미팅 시간 입력하기"])

    if option == "미팅 잡기":
        create_meeting()
    elif option == "미팅 시간 입력하기":
        input_meeting_time()

# 2. 미팅 잡기 화면
def create_meeting():
    st.header("미팅 잡기")
    name = st.text_input("당신의 이름을 입력하세요")
    date = st.date_input("가능한 미팅 날짜를 선택하세요")
    time = st.time_input("가능한 시간을 선택하세요")

    if st.button("미팅 일정 저장하기"):
        meeting_id = str(uuid.uuid4())  # 고유한 URL을 만들기 위해 UUID 사용
        meetings[meeting_id] = {
            "host": name,
            "dates": [date],
            "time": time,
        }
        st.success(f"미팅 일정이 저장되었습니다! 이 URL을 공유하세요: {st.experimental_set_query_params(id=meeting_id)}")

# 3. 공유된 URL로 접속한 사람의 UI
def input_meeting_time():
    query_params = st.experimental_get_query_params()
    meeting_id = query_params.get("id", [None])[0]

    if meeting_id and meeting_id in meetings:
        st.header(f"미팅 시간 입력하기 - 주관자: {meetings[meeting_id]['host']}")
        name = st.text_input("당신의 이름을 입력하세요")
        available_dates = meetings[meeting_id]['dates']
        selected_date = st.selectbox("가능한 미팅 날짜를 선택하세요", available_dates)
        time = st.time_input("가능한 시간을 선택하세요")

        if st.button("미팅 일정 저장하기"):
            # 미팅 정보 업데이트
            meetings[meeting_id]['dates'].append(selected_date)
            st.success(f"미팅 일정이 저장되었습니다! 이 URL을 공유하세요: {st.experimental_set_query_params(id=meeting_id)}")
    else:
        st.error("잘못된 URL입니다. 미팅 ID를 확인해주세요.")

# 앱 실행
if __name__ == "__main__":
    main()
