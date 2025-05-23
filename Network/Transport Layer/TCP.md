# TCP

### 특징

- **Point-to-point:**
  - 하나의 송신자와 하나의 수신자 간의 연결을 설정합니다.
  - 멀티캐스팅이나 브로드캐스팅은 지원하지 않습니다.
- **Reliable, in-order byte stream:**
  - 데이터 손실이나 순서 변경 없이 정확하게 전달합니다.
  - 데이터는 바이트 스트림으로 취급되며, 메시지 경계는 없습니다.
- **Full-duplex data:**
  - 양방향 통신을 지원하여 송신자와 수신자 모두 동시에 데이터를 주고받을 수 있습니다.
- **Cumulative ACKs:**
  - 수신자는 마지막으로 정상적으로 수신한 바이트까지의 모든 데이터를 확인했다는 응답을 보냅니다.
- **Pipelining:**
  - 여러 개의 데이터를 연속적으로 보내고, ACK를 기다리지 않고 다음 데이터를 전송하여 네트워크 효율성을 높입니다.
- **Connection-oriented:**
  - 데이터를 전송하기 전에 연결 설정(3-way handshake)을 수행하고, 연결 종료 시 연결 해제(4-way handshake)를 수행합니다.
- **Flow controlled:**
  - 수신자의 버퍼 오버플로우를 방지하기 위해 송신 데이터 양을 조절합니다.

## TCP Segment Structure (TCP 세그먼트 구조)

- **Source Port:**
  송신지 포트 번호
- **Destination Port:** 목적지 포트 번호
- **Sequence Number:** 세그먼트 데이터의 첫 번째 바이트 순서 번호
- **Acknowledgment Number:** 수신자가 다음으로 받기를 기대하는 바이트 순서 번호 (ACK 번호)
- **Header Length:** TCP 헤더의 길이
- **Flags:** 제어 비트 (SYN, ACK, FIN, RST, PSH, URG)
- **Window Size:** 수신 윈도우 크기 (수신 버퍼의 여유 공간)
- **Checksum:** 오류 검출을 위한 체크섬
- **Urgent Pointer:** 긴급 데이터 포인터
- **Options:** 옵션 필드 (MSS, Window Scale 등)
- **Data:** 실제 데이터

## TCP Sequence Numbers, ACKs (TCP 순서 번호, ACK)

- **Sequence Number:**  
  데이터의 순서를 나타내는 번호로, 데이터 손실이나 중복을 방지하고 순서를 재조립하는 데 사용됩니다.
- **Acknowledgment Number:**  
  수신자가 정상적으로 수신한 데이터의 마지막 순서 번호 + 1을 나타냅니다. 즉, 다음에 수신하기를 기대하는 순서 번호입니다.
- **Out-of-order segments 처리:**  
  TCP 명세에는 구체적인 방법이 정의되어 있지 않지만, 일반적으로 다음과 같은 방식으로 처리합니다.
  - **버퍼링:** 순서가 어긋난 세그먼트를 버퍼에 저장하고, 누락된 세그먼트가 도착하면 순서대로 재조립합니다.
  - **Selective ACK (SACK):** 특정 세그먼트만 정상적으로 수신했음을 알리는 ACK를 사용하여 재전송 효율성을 높입니다.

## TCP RTT (Round Trip Time)

- **Timeout 값 설정:**
  - **너무 짧은 경우:**  
    불필요한 재전송이 발생하여 네트워크 혼잡을 유발할 수 있습니다.
  - **너무 긴 경우:**  
    세그먼트 손실에 대한 반응이 늦어져 성능 저하를 초래할 수 있습니다.
- **RTT 측정 방법:**
  - **SampleRTT:**  
    세그먼트를 보내고 ACK를 받을 때까지의 시간을 측정합니다.
  - **EstimatedRTT:**  
    SampleRTT 기반으로 RTT를 추정합니다. (일반적으로 지수 가중 평균 필터(EWMA) 사용)
  - **TimeoutInterval:**  
    EstimatedRTT에 안전 마진을 더하여 설정합니다.  
    ( TimeoutInterval = EstimatedRTT + 4 \* DevRTT)

## TCP 통신 과정

1.  **3-way handshake (연결 설정):**
    - **SYN:** 클라이언트 -> 서버 (SYN 플래그 설정, 초기 순서 번호(ISN) 포함)
    - **SYN+ACK:** 서버 -> 클라이언트 (SYN 플래그, ACK 플래그 설정, 서버 ISN, 클라이언트 ISN+1)
    - **ACK:** 클라이언트 -> 서버 (ACK 플래그 설정, 서버 ISN+1)
2.  **Data transfer (데이터 전송):** 데이터를 세그먼트로 나누어 전송하고, ACK를 통해 확인합니다.
3.  **4-way handshake (연결 종료):**
    - **FIN:** 클라이언트 -> 서버
    - **ACK:** 서버 -> 클라이언트
    - **FIN:** 서버 -> 클라이언트
    - **ACK:** 클라이언트 -> 서버

### TCP 재전송 과정

- **Timeout:**  
  설정된 TimeoutInterval 동안 ACK를 받지 못하면 해당 세그먼트를 재전송합니다.
- **Fast Retransmit:**
  - 수신자가 순서에 맞지 않는 세그먼트를 받으면 중복 ACK (duplicate ACK)를 보냅니다.
  - 송신자가 동일한 ACK를 3개 (dupACK threshold) 받으면 Timeout이 발생하기 전에 해당 세그먼트를 재전송합니다.

## TCP 흐름 제어 (Flow Control)

네트워크 계층에서 데이터를 수신하는 속도가 응용 계층에서 데이터를 처리하는 속도보다 빠를 경우, 수신 버퍼 오버플로우가 발생할 수 있습니다.  
이는 데이터 손실을 야기하므로, TCP에서는 흐름 제어 메커니즘을 통해 이를 방지합니다.

**핵심 개념:**

- **수신 윈도우 (Receive Window, rwnd):**
  - 수신 측(Receiver)이 송신 측(Sender)에게 현재 자신이 얼마나 많은 데이터를 받을 수 있는지 알려주는 값입니다.
  - TCP 헤더의 segment 필드에 포함되어 전송됩니다.
- **흐름 제어 동작 방식:**
  - 송신 측은 수신 측으로부터 받은 rwnd 값을 기준으로 데이터를 전송합니다.
  - rwnd 값보다 큰 데이터를 한 번에 전송하지 않음으로써, 수신 측의 버퍼 오버플로우를 방지합니다.
- **동적인 조절:**

  - rwnd 값은 수신 측의 버퍼 상태에 따라 동적으로 변합니다.
  - 수신 측의 버퍼에 여유 공간이 생기면 rwnd 값을 늘려 송신 측에게 더 많은 데이터를 보낼 수 있음을 알리고,
  - 버퍼가 꽉 차면 rwnd 값을 줄이거나 0으로 설정하여 데이터 전송을 일시적으로 중단시킬 수 있습니다.

- **Zero Window Problem:**
  - 수신 측이 rwnd 값을 0으로 설정하여 송신 측에게 데이터 전송 중단을 요청했을 때, 송신 측은 더 이상 데이터를 전송할 수 없게 됩니다.
  - 하지만 수신 측의 버퍼 공간이 확보되어 rwnd 값이 0보다 커졌음에도 불구하고 이 정보가 송신 측에 제대로 전달되지 않을 수 있습니다.
  - 이러한 상황을 **Zero Window Problem**이라고 합니다.
  - 이를 해결하기 위해 TCP는 송신 측에서 주기적으로 1바이트의 데이터를 전송하여 수신 측의 rwnd 값을 확인하는 방식을 사용합니다.
  - 이 때 보내는 1바이트 데이터를 **Window Probe**라고 합니다.
