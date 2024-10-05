import streamlit as st
from datetime import datetime, timedelta
import uuid

# 전역 변수로 미팅 정보를 저장할 딕셔너리 (실제 앱에서는 DB를 사용하는 것이 적합)
meetings = {}

# 30분 간격의 시간 생성
def generate_time_slots():
    times = []
    start_time = datetime.strptime("00:00", "%H:%M")
    while start_time < datetime.strptime("23:59", "%H:%M"):
        times.append(start_time.strftime("%H:%M"))
        start_time += timedelta(minutes=30)
    return times

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
    
    # 여러 개의 날짜 선택 (달력)
    selected_dates = st.date_input(
        "가능한 미팅 날짜를 선택하세요", [], key="dates", help="Ctrl 또는 Shift 키를 눌러 복수 선택 가능", on_change=None, disabled=False, label_visibility="visible", min_value=None, max_value=None
    )

    # 30분 단위의 시간 선택 (여러 개 가능)
    time_slots = generate_time_slots()
    selected_times = st.multiselect(
        "가능한 미팅 시간을 선택하세요 (30분 단위)",
        time_slots,
        help="복수 선택 가능",
    )

    if st.button("미팅 일정 저장하기"):
        if not selected_dates or not selected_times:
            st.warning("날짜와 시간을 모두 선택해주세요.")
        else:
            meeting_id = str(uuid.uuid4())  # 고유한 URL을 만들기 위해 UUID 사용
            meetings[meeting_id] = {
                "host": name,
                "dates": selected_dates,
                "times": selected_times,
            }
            st.success(f"미팅 일정이 저장되었습니다! 이 URL을 공유하세요: {st.experimental_set_query_params(id=meeting_id)}")

# 3. 공유된 URL로 접속한 사람의 UI
def input_meeting_time():
    query_params = st.experimental_get_query_params()
    meeting_id = query_params.get("id", [None])[0]

    if meeting_id and meeting_id in meetings:
        st.header(f"미팅 시간 입력하기 - 주관자: {meetings[meeting_id]['host']}")
        name = st.text_input("당신의 이름을 입력하세요")

        # 주관자가 선택한 가능한 날짜들만 선택할 수 있도록 제약
        available_dates = meetings[meeting_id]['dates']
        selected_dates = st.multiselect("가능한 미팅 날짜를 선택하세요", available_dates, help="복수 선택 가능")

        # 주관자가 선택한 시간들만 선택할 수 있도록 제약
        available_times = meetings[meeting_id]['times']
        selected_times = st.multiselect("가능한 미팅 시간을 선택하세요", available_times, help="복수 선택 가능")

        if st.button("미팅 일정 저장하기"):
            if not selected_dates or not selected_times:
                st.warning("날짜와 시간을 모두 선택해주세요.")
            else:
                # 미팅 정보 업데이트
                meetings[meeting_id]['dates'].extend(selected_dates)
                meetings[meeting_id]['times'].extend(selected_times)
                st.success(f"미팅 일정이 저장되었습니다! 이 URL을 공유하세요: {st.experimental_set_query_params(id=meeting_id)}")
    else:
        st.error("잘못된 URL입니다. 미팅 ID를 확인해주세요.")

# 앱 실행
if __name__ == "__main__":
    main()
