from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('NanumGothic', '', 9)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, 'DOT AI 시스템 사용 가이드', new_x='LMARGIN', new_y='NEXT', align='C')
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('NanumGothic', '', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'- {self.page_no()} -', align='C')

    def chapter_title(self, title):
        self.set_font('NanumGothic', '', 16)
        self.set_text_color(51, 51, 51)
        self.cell(0, 10, title, new_x='LMARGIN', new_y='NEXT')
        self.ln(5)

    def section_title(self, title):
        self.set_font('NanumGothic', '', 12)
        self.set_text_color(80, 80, 80)
        self.cell(0, 8, title, new_x='LMARGIN', new_y='NEXT')
        self.ln(2)

    def body_text(self, text):
        self.set_font('NanumGothic', '', 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, text)
        self.ln(3)

font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
pdf = PDF()
pdf.add_font('NanumGothic', '', font_path)
pdf.set_auto_page_break(auto=True, margin=20)

# 표지
pdf.add_page()
pdf.ln(60)
pdf.set_font('NanumGothic', '', 28)
pdf.set_text_color(51, 51, 51)
pdf.cell(0, 15, 'DOT AI 시스템', new_x='LMARGIN', new_y='NEXT', align='C')
pdf.set_font('NanumGothic', '', 20)
pdf.cell(0, 12, '사용 가이드', new_x='LMARGIN', new_y='NEXT', align='C')
pdf.ln(30)
pdf.set_font('NanumGothic', '', 12)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 8, 'Document-Oriented Transformer', new_x='LMARGIN', new_y='NEXT', align='C')
pdf.cell(0, 8, '버전 1.0', new_x='LMARGIN', new_y='NEXT', align='C')
pdf.ln(40)
pdf.set_font('NanumGothic', '', 10)
pdf.cell(0, 6, '최종 업데이트: 2026년 2월', new_x='LMARGIN', new_y='NEXT', align='C')

# 1. 시스템 개요
pdf.add_page()
pdf.chapter_title('1. 시스템 개요')
pdf.section_title('1.1 DOT란?')
pdf.body_text('''DOT(Document-Oriented Transformer)는 기업 내부 문서 기반 AI 비서 시스템입니다. 폐쇄망(Air-gapped) 환경에서 운영 가능하도록 설계되어, 외부 인터넷 연결 없이도 모든 AI 기능을 활용할 수 있습니다.

DOT는 로컬 LLM(Large Language Model)을 기반으로 하여 기업의 민감한 데이터가 외부로 유출되지 않으면서도 최신 AI 기술의 혜택을 누릴 수 있도록 합니다.''')

pdf.section_title('1.2 시스템 구성')
pdf.body_text('''DOT 시스템은 다음과 같은 구성 요소로 이루어져 있습니다:

• Master Server: API 서버, 데이터베이스, 웹 프론트엔드 호스팅
• Worker Server: GPU 집약적 작업 처리 (이미지 생성, 음성 변환)
• LLM Engine: Llama 3 Korean Bllossom 8B 모델 기반 한국어 특화
• Vector DB: ChromaDB 기반 문서 임베딩 및 유사도 검색
• Message Queue: Redis + Celery 기반 비동기 작업 처리''')

pdf.section_title('1.3 운영 환경')
pdf.body_text('''• 운영 시간: 24시간 365일 (서버 가동 시)
• 권장 브라우저: Chrome, Edge, Firefox 최신 버전
• 네트워크: 내부망 전용 (외부 인터넷 연결 불필요)
• 접속 주소: http://[Master서버IP]:5173''')

pdf.section_title('1.4 하드웨어 요구사항')
pdf.body_text('''[Master Server]
• CPU: 8코어 이상
• RAM: 32GB 이상
• GPU: NVIDIA RTX 3080 이상 (VRAM 8GB+)
• 저장공간: SSD 500GB 이상

[Worker Server]
• CPU: 4코어 이상
• RAM: 16GB 이상
• GPU: NVIDIA RTX 3080 이상 (VRAM 8GB+)
• 저장공간: SSD 200GB 이상''')

# 2. 주요 기능
pdf.add_page()
pdf.chapter_title('2. 주요 기능')
pdf.section_title('2.1 AI 챗봇')
pdf.body_text('''자연어 기반 대화형 AI 비서입니다. 업무 관련 질문에 답변하고, 문서 내용을 요약하며, 아이디어 브레인스토밍을 지원합니다.

[특징]
• 실시간 스트리밍 응답 (토큰 단위 출력)
• 대화 기록 자동 저장 및 세션 관리
• RAG(검색 증강 생성) 기반 문서 참조 답변
• 한국어 특화 모델로 자연스러운 한국어 대화''')

pdf.section_title('2.2 문서 분석 (RAG)')
pdf.body_text('''PDF 문서를 업로드하면 AI가 내용을 분석하여 질문에 답변합니다.

[지원 형식] PDF
[처리 과정]
1. 문서 업로드 → 텍스트 추출
2. 텍스트 청킹 (500자 단위)
3. 임베딩 벡터 생성 (ko-sbert-nli 모델)
4. ChromaDB에 벡터 저장
5. 질문 시 유사도 검색 후 LLM에 컨텍스트 제공

[활용 예시]
• "이 계약서의 해지 조건이 뭐야?"
• "보고서에서 매출 관련 내용을 요약해줘"
• "규정집에서 휴가 관련 조항을 찾아줘"''')

pdf.section_title('2.3 이미지 생성')
pdf.body_text('''텍스트 프롬프트를 기반으로 AI 이미지를 생성합니다.

[모델] Stable Diffusion 기반 ComfyUI
[처리 시간] 약 20~40초 (해상도에 따라 상이)
[출력 해상도] 512x512 ~ 1024x1024

[프롬프트 작성 팁]
• 구체적인 묘사어 사용: "밝은 조명의 현대적인 사무실"
• 스타일 지정: "사실적인", "일러스트 스타일", "수채화 풍"
• 품질 키워드: "고품질", "선명한", "전문적인"''')

pdf.section_title('2.4 음성 변환 (STT)')
pdf.body_text('''음성 파일을 텍스트로 변환합니다. 회의 녹음, 인터뷰 등을 자동으로 전사하여 문서화할 수 있습니다.

[지원 형식] MP3, WAV, M4A, WEBM
[모델] Faster-Whisper Large V3
[지원 언어] 한국어, 영어 (자동 감지)
[처리 시간] 음성 길이의 약 10~20%

[활용 예시]
• 회의 녹음 → 회의록 자동 생성
• 인터뷰 녹음 → 텍스트 전사
• 강의 녹음 → 학습 자료 정리''')

pdf.add_page()
pdf.section_title('2.5 회의록 관리')
pdf.body_text('''음성 파일을 업로드하면 자동으로 텍스트 변환 후 AI가 회의 내용을 요약합니다.

[기능]
• 음성 → 텍스트 자동 변환
• AI 기반 회의 내용 요약
• 주요 결정사항 및 액션 아이템 추출
• 회의록 저장 및 검색''')

pdf.section_title('2.6 일정 관리')
pdf.body_text('''개인 및 팀 일정을 관리할 수 있는 캘린더 기능입니다.

[기능]
• 일정 등록, 수정, 삭제
• 월간/주간/일간 뷰 전환
• 일정 알림 설정
• 반복 일정 지원''')

# 3. 사용 방법
pdf.add_page()
pdf.chapter_title('3. 사용 방법')
pdf.section_title('3.1 로그인')
pdf.body_text('''1. 웹 브라우저에서 http://[서버IP]:5173 접속
2. 사번과 비밀번호 입력
3. "로그인" 버튼 클릭

* 초기 비밀번호는 관리자에게 문의하세요.
* 보안을 위해 최초 로그인 후 비밀번호를 변경해주세요.''')

pdf.section_title('3.2 챗봇 사용')
pdf.body_text('''1. 좌측 메뉴에서 "AI 챗봇" 선택
2. 하단 입력창에 질문 입력
3. Enter 키 또는 전송 버튼 클릭
4. AI 응답 확인 (실시간 스트리밍)

[세션 관리]
• 새 대화: 좌측 상단 "+" 버튼
• 이전 대화: 좌측 세션 목록에서 선택
• 대화 삭제: 세션 우측 휴지통 아이콘''')

pdf.section_title('3.3 문서 업로드')
pdf.body_text('''1. 챗봇 화면 또는 "문서 보관함"에서 업로드
2. PDF 파일 선택 (드래그 앤 드롭 가능)
3. 업로드 진행률 확인
4. 분석 완료 후 질문 가능

* 업로드된 문서는 "문서 보관함"에서 관리할 수 있습니다.
* 문서 삭제 시 해당 문서의 벡터 데이터도 함께 삭제됩니다.''')

pdf.section_title('3.4 이미지 생성')
pdf.body_text('''1. 좌측 메뉴에서 "이미지 생성" 선택
2. 프롬프트 입력 (원하는 이미지 설명)
3. "생성" 버튼 클릭
4. 생성 진행률 확인 (약 20~40초)
5. 완료 후 이미지 다운로드 가능''')

# 4. 사용 제한
pdf.add_page()
pdf.chapter_title('4. 사용 제한')
pdf.section_title('4.1 파일 업로드 제한')
pdf.body_text('''• 1일 최대 업로드 파일 수: 20개
• 파일당 최대 용량: 100MB
• 지원 형식: PDF (문서), MP3/WAV/M4A/WEBM (음성)
• 총 저장 용량: 사용자당 5GB''')

pdf.section_title('4.2 API 호출 제한')
pdf.body_text('''• 챗봇 질의: 분당 10회
• 이미지 생성: 1일 30회
• 음성 변환: 1일 20회
• 문서 분석: 1일 50회

* 제한 초과 시 일시적으로 기능이 제한됩니다.
* 업무상 추가 용량이 필요한 경우 관리자에게 문의하세요.''')

pdf.section_title('4.3 콘텐츠 제한')
pdf.body_text('''다음 콘텐츠는 시스템에서 처리되지 않거나 제한될 수 있습니다:

• 개인정보가 포함된 민감 문서 (별도 승인 필요)
• 저작권이 있는 이미지 생성 요청
• 부적절하거나 유해한 콘텐츠 생성 요청
• 시스템 리소스를 과도하게 사용하는 요청''')

pdf.section_title('4.4 동시 사용 제한')
pdf.body_text('''• 동시 접속 사용자: 최대 50명
• 동시 이미지 생성: 1건 (순차 처리)
• 동시 음성 변환: 1건 (순차 처리)

* GPU 작업(이미지, 음성)은 순차적으로 처리되어 대기 시간이 발생할 수 있습니다.''')

# 5. FAQ
pdf.add_page()
pdf.chapter_title('5. 자주 묻는 질문 (FAQ)')
pdf.section_title('Q1. 챗봇 응답이 느린 이유는?')
pdf.body_text('''A: 로컬 GPU에서 LLM을 구동하기 때문에 클라우드 서비스 대비 응답 속도가 다소 느릴 수 있습니다. 일반적으로 첫 토큰 출력까지 2~5초, 전체 응답 완료까지 10~30초가 소요됩니다.''')

pdf.section_title('Q2. 업로드한 문서를 챗봇이 인식하지 못해요.')
pdf.body_text('''A: 다음 사항을 확인해주세요:
• 문서 분석이 완료되었는지 확인 (진행률 100%)
• PDF 파일이 텍스트 기반인지 확인 (이미지 스캔 PDF는 미지원)
• 문서 내용과 관련된 질문인지 확인
• 문서를 삭제 후 다시 업로드 시도''')

pdf.section_title('Q3. 이미지 생성이 실패했어요.')
pdf.body_text('''A: 다음 원인이 있을 수 있습니다:
• Worker 서버 GPU 메모리 부족 → 잠시 후 재시도
• 부적절한 프롬프트 → 내용 수정 후 재시도
• 서버 일시 장애 → 관리자에게 문의''')

pdf.section_title('Q4. 음성 파일 변환이 안 돼요.')
pdf.body_text('''A: 지원되는 파일 형식(MP3, WAV, M4A, WEBM)인지 확인하세요. 파일 크기가 100MB를 초과하면 업로드가 제한됩니다. 음질이 너무 낮거나 잡음이 많은 경우 인식률이 떨어질 수 있습니다.''')

pdf.section_title('Q5. 대화 기록이 사라졌어요.')
pdf.body_text('''A: 대화 기록은 서버에 자동 저장됩니다. 좌측 세션 목록에서 이전 대화를 선택할 수 있습니다. 세션을 직접 삭제한 경우 복구가 불가능합니다.''')

pdf.section_title('Q6. 동시에 여러 작업을 할 수 있나요?')
pdf.body_text('''A: 챗봇 대화는 여러 세션에서 동시에 가능합니다. 다만 이미지 생성, 음성 변환 등 GPU 작업은 순차 처리되어 다른 사용자의 작업이 완료될 때까지 대기할 수 있습니다.''')

# 6. 문제 해결
pdf.add_page()
pdf.chapter_title('6. 문제 해결 가이드')
pdf.section_title('6.1 접속이 안 될 때')
pdf.body_text('''[증상] 웹 페이지가 열리지 않음

[해결 방법]
1. 서버 IP 주소가 올바른지 확인
2. 네트워크 연결 상태 확인 (내부망 연결 필수)
3. 방화벽에서 5173 포트가 허용되어 있는지 확인
4. 서버 관리자에게 서버 상태 문의''')

pdf.section_title('6.2 로그인이 안 될 때')
pdf.body_text('''[증상] 아이디/비밀번호 입력 후 로그인 실패

[해결 방법]
1. 사번과 비밀번호가 정확한지 확인
2. Caps Lock이 켜져 있지 않은지 확인
3. 브라우저 캐시 삭제 후 재시도
4. 비밀번호 초기화가 필요하면 관리자에게 문의''')

pdf.section_title('6.3 응답이 중단될 때')
pdf.body_text('''[증상] 챗봇 응답이 중간에 멈춤

[해결 방법]
1. 페이지 새로고침 (F5)
2. 새 세션에서 다시 질문
3. 질문을 더 짧게 수정하여 재시도
4. 지속적으로 발생하면 관리자에게 문의''')

pdf.section_title('6.4 파일 업로드 실패')
pdf.body_text('''[증상] 파일 업로드 중 오류 발생

[해결 방법]
1. 파일 크기가 100MB 이하인지 확인
2. 파일 형식이 지원되는지 확인 (PDF, MP3 등)
3. 파일명에 특수문자가 없는지 확인
4. 다른 브라우저에서 시도
5. 일일 업로드 한도 초과 여부 확인''')

pdf.section_title('6.5 이미지 생성 오류')
pdf.body_text('''[증상] 이미지 생성 요청 후 오류 메시지

[해결 방법]
1. 프롬프트에 부적절한 내용이 없는지 확인
2. 잠시 후 재시도 (GPU 리소스 부족일 수 있음)
3. 프롬프트를 단순화하여 재시도
4. 지속적으로 실패하면 관리자에게 문의''')

# 7. 문의처
pdf.add_page()
pdf.chapter_title('7. 문의처')
pdf.section_title('7.1 기술 지원')
pdf.body_text('''• 이메일: tech-support@company.com
• 내선번호: 1234
• 운영시간: 평일 09:00 ~ 18:00

[지원 범위]
• 시스템 접속 문제
• 기능 사용 관련 문의
• 오류 신고 및 버그 리포트''')

pdf.section_title('7.2 관리자 연락처')
pdf.body_text('''[시스템 관리자]
• 담당자: 홍길동
• 이메일: admin@company.com
• 내선번호: 5678

[권한 관리]
• 계정 생성/삭제 요청
• 비밀번호 초기화
• 용량 증설 요청''')

pdf.section_title('7.3 긴급 연락처')
pdf.body_text('''서버 장애 등 긴급 상황 발생 시:
• 긴급 핫라인: 010-1234-5678
• 24시간 운영

[긴급 상황 예시]
• 전체 서비스 접속 불가
• 데이터 유실 의심
• 보안 이슈 발견''')

pdf.section_title('7.4 피드백 및 건의')
pdf.body_text('''시스템 개선 의견이나 새로운 기능 제안:
• 이메일: feedback@company.com
• 사내 게시판: AI 시스템 건의 게시판

여러분의 소중한 의견이 DOT 시스템 발전에 큰 도움이 됩니다.''')

output_path = '/app/uploads/documents/AI_DOT_시스템_사용_가이드.pdf'
pdf.output(output_path)
print(f'PDF 생성 완료: {output_path}')
print(f'총 페이지 수: {pdf.page_no()}')
