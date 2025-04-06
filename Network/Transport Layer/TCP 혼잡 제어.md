# TCP 혼잡 제어

## AIMD (Additive Increase Multiplicative Decrease)

패킷 손실이 일어나기 전까지 전송량을 늘리고, 손실이 발생하면 전송량을 절반으로 줄이는 방식입니다.

- **동작 방식:**
  - **초기 단계 (Slow Start):**
    - 연결 설정 후, `cwnd` (congestion window)를 1 MSS (Maximum Segment Size)로 설정하고 전송을 시작합니다.
    - ACK를 받을 때마다 `cwnd`를 2배씩 증가시킵니다. (정확히는 ACK를 받을 때마다 ACK된 바이트 수만큼 `cwnd`에 더합니다.)
  - **증가 단계 (Additive Increase):**
    - `cwnd`가 임계점(`ssthresh`)에 도달하면, **Congestion Avoidance** 단계로 전환합니다.
    - ACK를 받을 때마다 `cwnd`를 1/`cwnd` 만큼 증가시킵니다. (1 RTT마다 1 MSS씩 증가)
    - 네트워크에 여유가 있다고 판단하면 전송량을 점진적으로 늘립니다.
  - **감소 단계 (Multiplicative Decrease):**
    - 패킷 손실이 감지되면 `cwnd`를 절반으로 줄입니다.
    - 네트워크 혼잡을 인지하고 전송량을 급격히 줄여 혼잡을 완화합니다.
  - **임계점 (Slow Start Threshold):**
    - `cwnd`가 임계점(`ssthresh`)에 도달하면, 증가 단계를 1 RTT마다 1 MSS씩 증가시키는 Congestion Avoidance 단계로 전환합니다.

## Delay-based TCP Congestion Control

패킷 손실뿐만 아니라 지연 시간 증가를 혼잡의 지표로 활용하는 방식입니다.

- **동작 방식:** RTT 변화를 모니터링하여 혼잡을 감지하고, `cwnd`를 조절합니다.

## ECN (Explicit Congestion Notification)

라우터가 혼잡을 감지하면 송신 호스트에게 명시적으로 알리는 방식입니다.

- **동작 방식:**
  - 라우터가 혼잡을 감지하면 IP 헤더의 ECN 필드를 설정합니다.
  - 수신 호스트는 ECN 필드가 설정된 패킷을 받으면 송신 호스트에게 이를 알립니다.
  - 송신 호스트는 ECN 신호를 받으면 `cwnd`를 줄여 혼잡을 완화합니다.

## TCP Fairness (TCP 공정성)

여러 TCP 연결이 하나의 병목 링크를 공유할 때, 각 연결에게 공평하게 대역폭을 분배하는 것을 의미합니다.

- **문제:** AIMD는 이상적인 공정성을 보장하지 못할 수 있습니다. RTT가 짧은 연결이 더 빠르게 `cwnd`를 증가시켜 더 많은 대역폭을 차지할 수 있습니다.
- **해결 방안:**
  - **Fair Queueing:** 라우터에서 각 연결에 대해 별도의 큐를 유지하고, 라운드 로빈 방식으로 패킷을 전송합니다.
  - **RED (Random Early Detection):** 라우터에서 큐 길이가 일정 수준을 넘으면 패킷을 임의로 폐기하여 혼잡을 미리 알립니다.
  - **ECN:** 위에서 설명한 ECN을 사용하여 혼잡을 명시적으로 알립니다.
