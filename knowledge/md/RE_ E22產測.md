# RE: E22產測

- Sender: ['=?big5?B?YmlsbF9jaGVuILOvq7Onyg==?= <bill_chen@accton.com>']
- Date: Wed, 1 Jul 2026 10:18:56 +0000
- Source File: RE_ E22產測.msg

---

## ✅ Summary
Dear Alan,
gLQ
,
HUswgs
TRD  Script,

---

## ✅ Clean Content
Dear Alan,
 
gLQ
, 
HUswgs
TRD  Script, 
٨SLD
E22 v12.5.db090-a185ec (Factory)
Thanks,
Bill

---

## ✅ Full Content
Dear Alan,
 
gLQ׫
, 
HUswgs
TRD & Script, 
·٨SLD
E22 v12.5.db090-a185ec (Factory)
Thanks,
Bill
 
From:
 alan2015_chen 
ݭ
 <> 
Sent:
 Wednesday, July 1, 2026 2:21 PM
 andy79_yang 
 <>; bill_chen 
 <>; eary_chen 
Aã
 <>; max_wu 
daa
 <>; earl_huang 
 <>; alex_chiang 
|
 <>
 lanqly_chou 
P
 <>
Subject:
 RE: E22
 
Hi Andy
1.
ݭn
AP
ݪ
SN
gť
,SSID
~|e{
E22-24G
P
 E22-5G(
5)
2. AP
IP
]w
192.168.2.2,
iH
ping
Lh
(
6 7)
3. 
Wzp
4. 
Wzp
5. 
g
ETH0
}
,
uݭnˬd
ETH0?   Lan1 lan2 lan3 waln0 wlan1 
ܥXӴNn
Tks.
Alan
From:
 andy79_yang 
 <

> 
Sent:
 Wednesday, July 1, 2026 11:37 AM
 alan2015_chen 
ݭ
 <

>; bill_chen 
 <

>; eary_chen 
Aã
 <

>; max_wu 
daa
 <

>; earl_huang 
 <

>; alex_chiang 
|
 <

>
 lanqly_chou 
P
 <

>
Subject:
 
^
: E22
 
Hi Alan
 
ЬݤU^
Ч󴫦o
2
ӫO
                   cd /acc
                   ./prepare_wifitest.sh
            
pG\U
iwinfo
|ݨUe
            admin@E22:/acc# iwinfo
wlan0     ESSID: "E22-5G"
          Access Point: 44:45:BA:1E:DA:3E
          Mode: Master  Channel: 36 (5.180 GHz)
          Center Channel 1: 50 2: unknown
          Tx-Power: 13 dBm  Link Quality: unknown/70
          Signal: unknown  Noise: -108 dBm
          Bit Rate: unknown
          Encryption: none
          Type: nl80211  HW Mode(s): 802.11nacax
          Hardware: unknown [Generic MAC80211]
          TX power offset: unknown
          Frequency offset: unknown
          Supports VAPs: yes  PHY name: phy0
 
wlan1     ESSID: "E22-24G"
          Access Point: 44:45:BA:1E:DA:3F
          Mode: Master  Channel: 6 (2.437 GHz)
          Center Channel 1: 8 2: unknown
          Tx-Power: 20 dBm  Link Quality: unknown/70
          Signal: unknown  Noise: -102 dBm
          Bit Rate: unknown
          Encryption: none
          Type: nl80211  HW Mode(s): 802.11bgnax
          Hardware: unknown [Generic MAC80211]
          TX power offset: unknown
          Frequency offset: unknown
          Supports VAPs: yes  PHY name: phy1
 
Ч󴫦o
2
ӫO
cd /acc
./prepare_wifitest_sta.sh 2g E22-24G
            
wifi reload
iH
ping 192.168.2.1
ݦSQs
AP
 
       3
4
OҨSTذ_
       5. command
榡pU
 e22_mac eth0 
00:11:22:33:44:55
 
1
2
Хg
MAC
bաAӤe
micronet
ͪy{Aq
sample
ӳg
mac
F~
(
ڦۤv쪺q
sample
]Og
)
 
b·нT{A
 
Best regards,
Andy
H
:
 alan2015_chen 
ݭ
 <

>
H
:
 2026
~
7
1
 
W
 09:07
:
 bill_chen 
 <

>; eary_chen 
Aã
 <

>; andy79_yang 
 <

>; max_wu 
daa
 <

>; earl_huang 
 <

>; alex_chiang 
|
 <

>
ƥ
:
 lanqly_chou 
P
 <

>
D
:
 RE: E22
 
Hi Bill
w쳭
,
QѸ
TRD 1.8
Oo{XӺð
1. AP
ݤU
/acc/prepare_wifitest.sh, 
]w\O_TiHP_
?
Φpˬd
? (
1)
2. DUT
ݤU
/acc/prepare_wifitest_sta.sh 2g E22-24G, 
O_]w\T
?
Φpˬd
? (
2)
3. DUT
ݤU
/acc/get_rssi.sh 2g,
X{
cat: can't open '/sys/kernel/debug/ieee80211/phy1/ath11k/htt_stats': Network is down,
Skˬd
RSSI(
2)
4. DUT
ݤU
iwconfig , Tx-Power
X{
- dBm
,
oӭȬO_T
? (
2)
5.  
g
MAC
ih᭫}
,
ŪXӪ
MAC
MgihP
(
3 4)
Aݤ@U
Tks.
Alan
From:
 alan2015_chen 
ݭ
Sent:
 Monday, June 29, 2026 11:23 AM
 bill_chen 
 <

>; eary_chen 
Aã
 <

>; andy79_yang 
 <

>; max_wu 
daa
 <

>; earl_huang 
 <

>; alex_chiang 
|
 <

>
 lanqly_chou 
P
 <

>
Subject:
 RE: E22
 
Hi Bill
P§se
,
t~
1.TRD
eO_sW
RSSI Pass 
P
 Fail
з
?
           2.
jc
DUT
P
Golden
ZP\覡O_Tw
? 
pϤFo
 
Hi Eary
O_iHAѤ@x
?
 
Tks.
Alan
From:
 bill_chen 
 <

>
Sent:
 Friday, June 26, 2026 5:27 PM
 alan2015_chen 
ݭ
 <

>; eary_chen 
Aã
 <

>; andy79_yang 
 <

>; max_wu 
daa
 <

>; earl_huang 
 <

>; alex_chiang 
|
 <

>
 lanqly_chou 
P
 <

>
Subject:
 RE: E22
 
Dear Eary and Alan,
 
E22
sW
LED, Button, RSSI
script
M
TRD, 
spU
 
E22 v12.5.db090-a185ec (Factory)
 
Thanks,
Bill
 
From:
 alan2015_chen 
ݭ
 <

>
Sent:
 Monday, June 15, 2026 8:49 AM
 bill_chen 
 <

>; eary_chen 
Aã
 <

>; andy79_yang 
 <

>; max_wu 
daa
 <

>; earl_huang 
 <

>
 lanqly_chou 
P
 <

>
Subject:
 RE: E22
 
Hi All
o䦳ǰDݭnQ
1.
      
Micronet
log
eu
RF
, 
S
LED. Button. Ethernet
,
T{
Micronet
O_
?
2.
      
Micronet 
log
MAC0,
oO
TRD
̭
eth0 MAC?
3.
~߲ո˫
,
O_d}fs
console? 
άOu
ssh
覡
4.
~߲ո˫O_ݭn
LED. Button. Throughput
RSSI
, 
T{
Tks.
Alan
From:
 bill_chen 
 <

>
Sent:
 Friday, June 12, 2026 4:27 PM
 eary_chen 
Aã
 <

>; andy79_yang 
 <

>; alan2015_chen 
ݭ
 <

>; max_wu 
daa
 <

>; earl_huang 
 <

>
 lanqly_chou 
P
 <

>
Subject:
 RE: E22
 
Dear Eary,
 
E22 12.5.93 
FW
P
 TRD
wҧ
, 
spU
 
E22 v12.5.db090-a185ec (Factory)
 
Thanks,
Bill
 
From:
 bill_chen 
Sent:
 Wednesday, June 10, 2026 1:50 PM
 eary_chen 
Aã
 <

>; andy79_yang 
 <

>; alan2015_chen 
ݭ
 <

>; max_wu 
daa
 <

>; earl_huang 
 <

>
 lanqly_chou 
P
 <

>
Subject:
 RE: E22
 
Dear Eary,
 
ثe
 E22 12.5.93 
FW
P
 TRD 
iդAwp駹
 
Thanks,
Bill
 
From:
 eary_chen 
Aã
 <

>
Sent:
 Wednesday, June 10, 2026 9:51 AM
 andy79_yang 
 <

>; bill_chen 
 <

>; alan2015_chen 
ݭ
 <

>; max_wu 
daa
 <

>; earl_huang 
 <

>
Subject:
 E22
 
Hi, Andy/Bill,
а
E22 
̫nWu
code
nF
?
 
Thanks,
Eary
