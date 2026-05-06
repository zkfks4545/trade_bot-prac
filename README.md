📑 [최종 기획서] 미국 주식 실시간 뉴스 돌파 단타 봇 (소액 실전용)

1. 개요 및 운영 철학

목표: 해외 뉴스 및 국내 속보 텔레그램 채널에서 미국 주식 호재 발생 시, 실시간으로 감지하여 소수점 시장가 매수 후 당일 청산하는 단타 알고리즘 검증.

운용 환경: 한국투자증권 봇 전용 서브 위탁계좌를 개설하여 소액(예: 10만 원)만 입금 후 철저히 자산을 격리하여 운영.

거래 전략: 100% 롱(Long, 매수) 전략만 구동 (소수점 거래 제약 및 안전성 확보).

2. 핵심 알고리즘 루프 (Rule)

작동 시간: 한국 시간 기준 밤 9시 30분 ~ 새벽 5시 (미국 정규장 및 서머타임 대응)

진입 조건: 1. 지정된 2개 텔레그램 채널에서 미국 주식 티커(TSLA, NVDA 등)가 포함된 속보 감지.

2. 본문에 지정한 호재 키워드(Acquisition, Merger, Earnings Beat, Contract, 승인 등) 포함 여부 검증.

3. 최근 10분 내 동일 종목 매매 이력 없고, 계좌에 미보유 중인 종목인 경우 진입.

자금 관리: 회당 최대 진입 금액 제한 (예: 회당 $10~20 내외로 소수점 매수).

청산 조건 (트레일링 스탑 & 타임컷):

손절선: 진입가 대비 -1.5% 도달 시 칼손절.

트레일링 익절: 주가가 진입가 대비 +2%를 돌파하는 순간 감시 시작 ➔ 최고점 대비 1% 하락 시 전량 익절 청산 (수익 극대화).

타임컷 (당일 청산): 새벽 4시 50분(장 마감 10분 전)까지 미청산된 종목은 무조건 시장가 일괄 청산.

일일 보고: 정규장 종료 및 정산이 끝난 새벽 5시 10분에 내 텔레그램으로 최종 하루 정산서(수익률, 잔고) 발송 후 봇 자동 일시 정지.

📁 프로젝트 디렉토리 구조

아래 구조로 프로젝트 폴더를 구성합니다. 데이터베이스 대신 가벼운 JSON 파일과 CSV 파일로 가상 장부 및 설정을 관리합니다.

<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #0f172a; color: #e2e8f0; padding: 25px; border-radius: 8px;">

  <h1 style="color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 10px;">🚀 hantu-us-bot</h1>
  <p style="color: #cbd5e1;">한국투자증권 Open API를 활용한 소수점 미국 주식 실시간 뉴스 돌파 단타 자동매매 시스템입니다.</p>

  <div style="background-color: #1e293b; border-left: 4px solid #38bdf8; padding: 15px; border-radius: 0 8px 8px 0; margin: 20px 0;">
    <p style="margin: 0; font-size: 0.95rem; color: #94a3b8;">
      <strong style="color: #38bdf8;">💡 운영 철학:</strong> 
      철저한 자산 격리를 위해 <strong>봇 전용 서브 계좌</strong>를 사용하며, <strong>100% 롱(Long) 전략</strong>과 당일 새벽 장 마감 전 모든 주식을 전량 정리하는 <strong>당일 청산(오버나잇 배제)</strong> 룰을 기본으로 합니다.
    </p>
  </div>

  <h2 style="color: #34d399; border-left: 4px solid #34d399; padding-left: 10px; margin-top: 30px;">📂 프로젝트 디렉토리 트리 구조</h2>
  
  <pre style="background-color: #1e293b; border: 1px solid #475569; border-radius: 8px; padding: 20px; font-family: 'Courier New', Courier, monospace; color: #38bdf8; line-height: 1.6; overflow-x: auto;">
hantu-us-bot/
│
├── 📄 <span style="color: #34d399; font-weight: bold;">.env</span>                  <span style="color: #94a3b8;"># App Key, 계좌번호 등 민감한 개인보안 정보 격리</span>
├── 📄 <span style="color: #34d399; font-weight: bold;">config.json</span>           <span style="color: #94a3b8;"># 손익절 비율, 1회 투자 비중, 필터링 키워드 관리 (유지보수 핵심)</span>
├── 📄 <span style="color: #34d399; font-weight: bold;">requirements.txt</span>      <span style="color: #94a3b8;"># 파이썬 의존성 패키지 설치 가이드</span>
│
├── 📄 <span style="color: #34d399; font-weight: bold;">main.py</span>               <span style="color: #94a3b8;"># 봇 메인 실행 파일 (전체 프로세스 기동 및 비동기 루프 핸들링)</span>
├── 📄 <span style="color: #34d399; font-weight: bold;">hantu_api.py</span>          <span style="color: #94a3b8;"># 한국투자증권 실서버 API 통신 (토큰 갱신, 실시간 잔고/시세, 매매 주문)</span>
├── 📄 <span style="color: #34d399; font-weight: bold;">telegram_monitor.py</span>   <span style="color: #94a3b8;"># 텔레그램 실시간 속보 채널 스니핑, 티커 및 호재 필터링</span>
└── 📄 <span style="color: #34d399; font-weight: bold;">scheduler.py</span>          <span style="color: #94a3b8;"># 미국 정규장 타임라인 감시, 강제 당일 청산 및 새벽 5시 정산 보고</span>
  </pre>

  <h2 style="color: #34d399; border-left: 4px solid #34d399; padding-left: 10px; margin-top: 30px;">📝 파일별 세부 명세</h2>
  <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
    <thead>
      <tr style="background-color: #1e293b; color: #38bdf8; border-bottom: 2px solid #475569;">
        <th style="padding: 12px; text-align: left;">파일명</th>
        <th style="padding: 12px; text-align: left;">주요 역할 및 설명</th>
      </tr>
    </thead>
    <tbody style="color: #cbd5e1;">
      <tr style="border-bottom: 1px solid #334155;">
        <td style="padding: 12px; font-family: monospace; color: #34d399; font-weight: bold;">.env</td>
        <td style="padding: 12px;">공개되어서는 안 되는 개인 API Key, 계좌 정보, 개인 텔레그램 봇 토큰 및 텔레그램 개발 ID를 로컬에 격리해두는 저장소입니다.</td>
      </tr>
      <tr style="border-bottom: 1px solid #334155;">
        <td style="padding: 12px; font-family: monospace; color: #34d399; font-weight: bold;">config.json</td>
        <td style="padding: 12px;">코드를 매번 뜯고 배포하는 번거로움을 제거하기 위한 동적 룰셋입니다. 익절 트리거(+2%), 트레일링 스탑, 칼손절(-1.5%), 1회 투자액($15), 뉴스 필터링 키워드가 선언되어 있습니다.</td>
      </tr>
      <tr style="border-bottom: 1px solid #334155;">
        <td style="padding: 12px; font-family: monospace; color: #34d399; font-weight: bold;">scheduler.py</td>
        <td style="padding: 12px;">새벽 4시 50분에 남아있는 잔고를 일괄 시장가 매도하여 강제 청산(오버나잇 방지)을 실행하고, 장 마감 시점인 새벽 5시 10분에 텔레그램으로 정산 보고를 쏘는 시간제어 루프입니다.</td>
      </tr>
    </tbody>
  </table>

</div>
