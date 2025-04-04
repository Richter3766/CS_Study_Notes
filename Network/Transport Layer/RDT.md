# RDT(Reliable Data transfer)

RDT(Reliable Data Transfer) 프로토콜은 신뢰할 수 없는 하위 계층에서 신뢰할 수 있는 데이터 전송을 보장하기 위해 다양한 기법을 사용합니다.

## 1. ACK 메세지

수신자는 패킷을 오류 없이 받았음을 송신자에게 알리기 위해 ACK(acknowledgment) 메세지를 전송합니다.  
송신자는 특정 패킷에 대한 ACK를 수신함으로써 해당 패킷이 정상적으로 도착했음을 인지할 수 있습니다.

### ACK가 유실되거나 늦어 오지 않을 경우

ACK가 유실되거나 수신자가 패킷을 받지 못한 경우, 송신자는 타임아웃(time-out) 메커니즘을 사용하여 일정 시간 내에 ACK를 받지 못하면 해당 패킷이 유실된 것으로 간주하고 재전송합니다.

### 패킷을 제대로 받아 ACK를 보냈는데 유실된 경우

수신자가 패킷을 정상적으로 받았지만 ACK가 유실된 경우, 송신자는 중복 패킷을 전송할 수 있습니다.  
이를 방지하기 위해 송신자와 수신자는 각 패킷에 시퀀스 번호를 부여합니다.  
수신자는 이미 수신한 패킷의 시퀀스 번호를 기억하고, 중복된 패킷을 받았을 때 무시합니다.  
이 방법으로 중복 패킷 문제를 해결할 수 있습니다.

## 2. 오염된 패킷

패킷이 전송 도중 오염될 수 있는 경우, 수신자는 패킷의 무결성을 확인해야 합니다. 이를 위해 다음과 같은 메커니즘을 사용할 수 있습니다.

### 오류 검출 기법

송신자는 패킷에 오류 검출 코드를 추가하여 전송합니다.  
가장 많이 사용되는 방법은 **체크섬**(checksum) 또는 **CRC**(Cyclic Redundancy Check)입니다.  
수신자는 패킷을 수신한 후, 오류 검출 코드를 확인하여 패킷이 오염되었는지 여부를 판단합니다.

- **체크섬**:  
  송신자는 데이터의 비트 합을 계산하여 체크섬을 생성하고, 이를 패킷에 포함시킵니다.  
  수신자는 수신한 데이터와 체크섬을 비교하여 오류를 검출합니다.

- **CRC**:  
  더 강력한 오류 검출 기법으로, 송신자는 다항식을 사용해 데이터를 변환하여 CRC 값을 생성합니다.  
  수신자는 동일한 다항식을 사용해 수신한 데이터의 CRC 값을 계산하여 비교합니다.

### 오염된 패킷 처리

수신자가 패킷의 오류를 검출한 경우, 해당 패킷을 폐기하고 NAK(negative acknowledgment) 메세지를 송신자에게 전송합니다.  
송신자는 NAK를 수신하면 해당 패킷을 재전송합니다. 이를 통해 오염된 패킷 문제를 해결할 수 있습니다.

## NAK-Free

NAK를 보내는 대신 송신자 측에서 해당 패킷에 대해 타임아웃이 되도록 유도하여 다시 패킷을 받기도 합니다.  
또는 다음 패킷의 ACK에 이전 패킷의 시퀀스 넘버를 포함시키지 않는 방법도 있습니다.
이를 통해 불필요한 네트워크 오버헤드를 줄일 수 있습니다.
