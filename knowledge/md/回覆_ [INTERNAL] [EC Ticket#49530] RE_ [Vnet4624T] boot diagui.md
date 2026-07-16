# 回覆: [INTERNAL] [EC Ticket#49530] RE: [Vnet4624T] boot diagui

- Sender: ['=?utf-8?B?Y2hpYW5nIOe+heaZguW8tw==?= <>']
- Date: Tue, 9 Jun 2026 16:02:11 +0000
- Source File: 回覆_ [INTERNAL] [EC Ticket#49530] RE_ [Vnet4624T] boot diagui.msg

---

## ✅ Summary
Hi Enco,
Sure, I understand your point.
Thank you for your valuable suggestion.
Best Regards,
/Chiang

---

## ✅ Clean Content
Hi Enco,
Sure, I understand your point.
Thank you for your valuable suggestion.
Best Regards,
/Chiang   
寄件者: 
enco 劉升順 
日期: 
星期二, 2026年6月9日 晚上10:56
收件者: 
chiang 羅時強 
alex_chiang 江育誠  kelly 孫惠珍  sam_wu 吳生三 
主旨: 
RE: INTERNAL EC Ticket49530 RE: Vnet4624T boot diagui
Chiang,
I suggest we need to explain on the SOP whenever they are having the issue, what action they should take,
otherwise they may simply put into the package and ship to customer, that even worse.
 
 
 
 
 
 
Regards,
Enco

---

## ✅ Full Content
Hi Enco,
Sure, I understand your point.
Thank you for your valuable suggestion.
Best Regards,
/Chiang   
寄件者: 
enco 劉升順 <>
日期: 
星期二, 2026年6月9日 晚上10:56
收件者: 
chiang 羅時強 <>
alex_chiang 江育誠 <>; kelly 孫惠珍 <>; sam_wu 吳生三 <>
主旨: 
RE: [INTERNAL] [EC Ticket#49530] RE: [Vnet4624T] boot diagui
Chiang,
I suggest we need to explain on the SOP whenever they are having the issue, what action they should take,
otherwise they may simply put into the package and ship to customer, that even worse.
 
 
 
 
 
 
Regards,
Enco
 
From:
 chiang 
羅時強
 <>
Sent:
 Tuesday, June 9, 2026 11:54 PM
 enco 
劉升順
 <>
 alex_chiang 
江育誠
 <>; kelly 
孫惠珍
 <>; sam_wu 
吳生三
 <>
Subject:
 
回覆
: [INTERNAL] [EC Ticket#49530] RE: [Vnet4624T] boot diagui
 
 
Hi Enco,
That's the same question I have as well.
We suspect the operator found a cosmetic issue and needed to replace the cover/base assembly. After the rework was completed, the unit was returned to FT for verification, 
which led to the FT test being run again. 
 
 
Best Regards,
/Chiang   
 
寄件者
: 
enco 
劉升順
 <

>
日期
: 
星期二
, 2026
年
6
月
9
日
 
晚上
10:10
收件者
: 
chiang 
羅時強
 <

>
: 
alex_chiang 
江育誠
 <

>; kelly 
孫惠珍
 <

>; sam_wu 
吳生三
 <

>
主旨
: 
RE: [INTERNAL] [EC Ticket#49530] RE: [Vnet4624T] boot diagui
Chiang,
From your update, it prevents the operator from running the FT test.
But, do we know why this operator wants to re-run the FT test after the FDL is done?
Is there something the operator is seeking for confirmation which trigger them to do FT again?
 
 
 
 
 
 
Regards,
Enco
 
From:
 chiang 
羅時強
 <

>
Sent:
 Tuesday, June 9, 2026 11:02 PM
 enco 
劉升順
 <

>
 alex_chiang 
江育誠
 <

>; kelly 
孫惠珍
 <

>; sam_wu 
吳生三
 <

>
Subject:
 
回覆
: [INTERNAL] [EC Ticket#49530] RE: [Vnet4624T] boot diagui
 
Hi Enco,
Process:
FT =>FDL => OQC => Packing
Before:
The FT test script would detect whether the unit has diagnostic code . If no, the script would automatically program the code and then proceed with testing.
 
After:
The FT test script has been modified to remove the automatic diagnostic code detection and programming function. If a unit is returned to the FT station without diagnostic code, 
the FT test will not run and will display a "Fail" message.
 
Best Regards,
/Chiang   
 
寄件者
: 
enco 
劉升順
 <

>
日期
: 
星期二
, 2026
年
6
月
9
日
 
晚上
9:36
收件者
: 
chiang 
羅時強
 <

>
: 
alex_chiang 
江育誠
 <

>; kelly 
孫惠珍
 <

>; sam_wu 
吳生三
 <

>
主旨
: 
RE: [INTERNAL] [EC Ticket#49530] RE: [Vnet4624T] boot diagui
Chiang,
Can you explain to me what modifications we have done to our test program to prevent this?
 
 
 
 
 
 
Regards,
Enco
 
From:
 chiang 
羅時強
 <

>
Sent:
 Tuesday, June 9, 2026 10:30 PM
 enco 
劉升順
 <

>
 alex_chiang 
江育誠
 <

>; kelly 
孫惠珍
 <

>; sam_wu 
吳生三
 <

>
Subject:
 
回覆
: [INTERNAL] [EC Ticket#49530] RE: [Vnet4624T] boot diagui
 
Hi Enco,
Sorry for the issue that occurred.
We have implemented a system-level corrective action to prevent recurrence. 
The test program has already been modified and implemented to thoroughly address and resolve the issue.
 
 
 
Best Regards,
/Chiang   
 
寄件者
: 
enco 
劉升順
 <

>
日期
: 
星期二
, 2026
年
6
月
9
日
 
下午
1:46
收件者
: 
chiang 
羅時強
 <

>
: 
alex_chiang 
江育誠
 <

>; kelly 
孫惠珍
 <

>; sam_wu 
吳生三
 <

>
主旨
: 
FW: [INTERNAL] [EC Ticket#49530] RE: [Vnet4624T] boot diagui
Chiang,
This issue happened twice, there mush be something we can improve to prevent this, what do you think?
The model name is: Vnet4624T.
 
產線人員將完成
OQC
的機台，拿回
FT
站別單獨重測，導致機台回到
Diag mode (Cusomer OS missing)
Attachment(s)
Missing Customer OS.pptx
 
 
 
 
Regards,
Enco
 
From:
 support <

>
Sent:
 Friday, June 5, 2026 5:08 PM
 kelly 
孫惠珍
 <

>; ken_tseng 
曾志鏘
 <

>; serena_hung 
洪慧純
 <

>; kc_fan 
范光啓
 <

>
Subject:
 Re: [INTERNAL] [EC Ticket#49530] RE: [Vnet4624T] boot diagui
 
[WARNING!!] Mail from outside!!  Don’t click on links or attachments without confirmation.
*********************************************************************************
##- Please type your reply above this 
[INTERNAL]
YOU ARE A "FOLLOWER" ON THIS REQUEST (EC Ticket 
#49530
). Reply to this email to add an internal note to the request.
Ticket Requester/Submitter: "gina_lin 
林美均
" (

)
Assignee: "tiffany_liu 
劉玉萱
"
CCs on ticket:
"ITUS_Junehun Kim" <

>, "ITUS_Si_Yano" <

>, "Sg Lee" <

>, "kelly 
孫惠珍
" <

>, "tiffany_liu 
劉玉萱
" <

>
[INTERNAL]
tiffany_liu 
劉玉萱
 (Tech Support System)
Jun 5, 2026, 17:07 GMT+8
Private note
<Update>
 
VN
提供的
RCA for record.
Root Cause: 
產線人員並未遵守測試流程
: FT =>FDL => OQC => Packing
 
產線人員將完成
OQC
的機台，拿回
FT
站別單獨重測，導致機台回到
Diag mode (Cusomer OS missing)
Attachment(s)
Missing Customer OS.pptx
 
tiffany_liu 
劉玉萱
 (Tech Support System)
Jun 2, 2026, 16:46 GMT+8
Private note
<Update>
 
VN 
6/12
前完成目前庫存
1000
多台的
Sorting
確保機台開機可以順利進到客戶
OS
 
 
-----Original Message-----
From: gina_lin 
林美均
 <

> 
Sent: Tuesday, June 2, 2026 3:34 PM
陈氏银
 Trần Thị Ngân <

>; tiffany_liu 
劉玉萱
 <

>
何峻維
 <

>; kc_fan 
范光啓
 <

>; kelly 
孫惠珍
 <

>; eric1_lin 
林威廷
 <

>; benson_peng 
彭智德
 <

>; jack_chuang 
莊永豪
 <

>; cy_chao 
趙中揚
 <

>; wenqiang_zhang 
张文强
 <

>; lu_lin 
林吉裕
 <

>; xiaofei_lin 
林小飞
 <

>; chungtai_liu 
劉中泰
 <

>; andy_huang 
黃清揚
 <

>; chungtai_liu 
劉中泰
 <

>; chiang 
羅時強
 <

>; pamela_kuo 
郭玉屏
 <

>; debby_huang 
黃文
 <

>
Subject: RE: ITUS Ticket#49530 [Vnet4624T] boot diagui 
Importance: High
 
Hi Vanila, Hi Tiffany,
 
Since iTUS requests us to deliver 1,080units during the mid of June, we have to pack these units by June 15th.
Please kindly help to rework them as soon as possible.
 
Thank you!
 
Best Regards,
Gina Lin   
 
 
 
-----Original Message-----
From: vanila_tran 
陈氏银
 Trần Thị Ngân <

>
Sent: Tuesday, June 2, 2026 3:17 PM
劉玉萱
 <

>
何峻維
 <

>; kc_fan 
范光啓
 <

>; kelly 
孫惠珍
 <

>; gina_lin 
林美均
 <

>; eric1_lin 
林威廷
 <

>; benson_peng 
彭智德
 <

>; jack_chuang 
莊永豪
 <

>; cy_chao 
趙中揚
 <

>; wenqiang_zhang 
张文强
 <

>; lu_lin 
林吉裕
 <

>; xiaofei_lin 
林小飞
 <

>; chungtai_liu 
劉中泰
 <

>; andy_huang 
黃清揚
 <

>; chungtai_liu 
劉中泰
 <

>; chiang 
羅時強
 <

>
Subject: RE: ITUS Ticket#49530 [Vnet4624T] boot diagui
 
Hi Tiffany
I'll create a rework order and retest all of unit in OQC station. Then I'll provide 8D report to you ASAP
 
Best Regards
---------------
Vanila_CQA Dept
Vietnam Accton Technology Co.,Ltd
 
 
-----Original Message-----
From: tiffany_liu 
劉玉萱
 <

>
Sent: Monday, June 1, 2026 4:13 PM
陈氏银
 Trần Thị Ngân <

>
何峻維
 <

>; kc_fan 
范光啓
 <

>; kelly 
孫惠珍
 <

>; gina_lin 
林美均
 <

>; eric1_lin 
林威廷
 <

>; benson_peng 
彭智德
 <

>; jack_chuang 
莊永豪
 <

>; cy_chao 
趙中揚
 <

>; wenqiang_zhang 
张文强
 <

>; lu_lin 
林吉裕
 <

>; xiaofei_lin 
林小飞
 <

>; chungtai_liu 
劉中泰
 <

>; andy_huang 
黃清揚
 <

>; chungtai_liu 
劉中泰
 <

>; chiang 
羅時強
 <

>
Subject: RE: ITUS Ticket#49530 [Vnet4624T] boot diagui
 
Hi Vanila,
 
In addition to identifying the root cause, the top priority is to prevent any further defective units from reaching the customer.
Please help confirm the current inventory quantity for this model and help to rework to check power-on status (do not perform OQC test.) Thank you
 
 
 
Best Regards,
Tiffany Liu | Engineer of Product & Quality Management Div
Email: 

 | Contact: +886 3 563 8888 
#5034
 
 
tiffany_liu 
劉玉萱
 (Tech Support System)
Jun 1, 2026, 17:14 GMT+8
Private note
<Update>
 
VN
確認流程
OQC
後不再上電，直接包裝
Nand Flash (A) 
也沒有
Quality issue 
紀錄
 
Next step:
1. 
請
VN
拿兩台庫存出來看開機情況
2. 
拉目前庫存機台出來檢查開機狀態
 
 
From: tiffany_liu 
劉玉萱
 
Sent: Monday, June 1, 2026 5:13 PM
陈氏银
 Trần Thị Ngân <

>
何峻維
 <

>; kc_fan 
范光啓
 <

>; kelly 
孫惠珍
 <

>; gina_lin 
林美均
 <

>; eric1_lin 
林威廷
 <

>; benson_peng 
彭智德
 <

>; jack_chuang 
莊永豪
 <

>; cy_chao 
趙中揚
 <

>; wenqiang_zhang 
张文强
 <

>; lu_lin 
林吉裕
 <

>; xiaofei_lin 
林小飞
 <

>; chungtai_liu 
劉中泰
 <

>; andy_huang 
黃清揚
 <

>; chungtai_liu 
劉中泰
 <

>; chiang 
羅時強
 <

>
Subject: RE: ITUS Ticket#49530 [Vnet4624T] boot diagui
 
Hi Vanila,
 
In addition to identifying the root cause, the top priority is to prevent any further defective units from reaching the customer.
Please help confirm the current inventory quantity for this model and help to rework to check power-on status (do not perform OQC test.) Thank you
 
 
 
Best Regards,
Tiffany Liu | Engineer of Product & Quality Management Div
Email: 

 | Contact: +886 3 563 8888 
#5034
 
 
-----Original Message-----
From: vanila_tran 
陈氏银
 Trần Thị Ngân <

>
Sent: Monday, June 1, 2026 2:46 PM
劉玉萱
 <

>
何峻維
 <

>; kc_fan 
范光啓
 <

>; kelly 
孫惠珍
 <

>; gina_lin 
林美均
 <

>; eric1_lin 
林威廷
 <

>; benson_peng 
彭智德
 <

>; jack_chuang 
莊永豪
 <

>; cy_chao 
趙中揚
 <

>; wenqiang_zhang 
张文强
 <

>; lu_lin 
林吉裕
 <

>; xiaofei_lin 
林小飞
 <

>; chungtai_liu 
劉中泰
 <

>; andy_huang 
黃清揚
 <

>; chungtai_liu 
劉中泰
 <

>; chiang 
羅時強
 <

>
Subject: RE: ITUS Ticket#49530 [Vnet4624T] boot diagui
 
Hi Tiffany,
 
At present, we have not identified any potential risk at the factory that could lead to the missing Customer OS issue.
After reviewing the records following the OQC test, I checked whether there was any history of units being powered on or tested again. However, no test logs were found after the OQC stage.
So far, no abnormalities have been identified at the factory.
 
Please refer to the attached analysis report for details.
 
Best Regards
---------------
Vanila_CQA Dept
Vietnam Accton Technology Co.,Ltd
 
 
tiffany_liu 
劉玉萱
 (Tech Support System)
May 28, 2026, 15:19 GMT+8
Private note
<Update>
 
1.
待
VN
內部調查可能原因
:
 
·
        
請協助盡快調查產線
FDL
流程，是否有瑕疵
?
·
        
流程是否為
:FT=>FDL=>OQC=>
直接包裝不再上電
?
·
        
Nand Flash
是否有
quality
疑慮的紀錄
?
 
2.
待客戶寄回失效機台
 
From: tiffany_liu 
劉玉萱
 
Sent: Tuesday, May 26, 2026 5:45 PM
陈氏银
 Trần Thị Ngân <

>
何峻維
 <

>; kc_fan 
范光啓
 <

>; kelly 
孫惠珍
 <

>; gina_lin 
林美均
 <

>; eric1_lin 
林威廷
 <

>; benson_peng 
彭智德
 <

>; jack_chuang 
莊永豪
 <

>; cy_chao 
趙中揚
 <

>; wenqiang_zhang 
张文强
 <

>; lu_lin 
林吉裕
 <

>; xiaofei_lin 
林小飞
 <

>; chungtai_liu 
劉中泰
 <

>; andy_huang 
黃清揚
 <

>; chungtai_liu 
劉中泰
 <

>; chiang 
羅時強
 <

>
Subject: RE: ITUS Ticket#49530 [Vnet4624T] boot diagui
 
Hi Vanila,
 
所以我們才要想辦法找到原因
...
 
OQC LOG
都有成功進到客戶
OS
1.
請協助盡快調查產線
FDL
流程，是否有瑕疵
?
流程是否為
:FT=>FDL=>OQC=>
直接包裝不再上電
?
 
2.Nand Flash
是否有
quality
疑慮的紀錄
?
 
 
Best Regards,
Tiffany Liu | Engineer of Product & Quality Management Div
Email: 

 | Contact: +886 3 563 8888 
#5034
 
 
 
No.1, Creation Road 3, Hsinchu Science Park, Hsinchu City 300093, Taiwan, R.O.C.
 
Web: 
www.edge-core.com
 
 
 
 
 
 
-----Original Message-----
From: vanila_tran 
陈氏银
 Trần Thị Ngân <

>
Sent: Tuesday, May 26, 2026 5:22 PM
劉玉萱
 <

>
何峻維
 <

>; kc_fan 
范光啓
 <

>; kelly 
孫惠珍
 <

>; gina_lin 
林美均
 <

>; eric1_lin 
林威廷
 <

>; benson_peng 
彭智德
 <

>; jack_chuang 
莊永豪
 <

>; cy_chao 
趙中揚
 <

>; wenqiang_zhang 
张文强
 <

>; lu_lin 
林吉裕
 <

>; xiaofei_lin 
林小飞
 <

>; chungtai_liu 
劉中泰
 <

>; andy_huang 
黃清揚
 <

>; chungtai_liu 
劉中泰
 <

>; chiang 
羅時強
 <

>
Subject: RE: ITUS Ticket#49530 [Vnet4624T] boot diagui
 
Hi Tiffany
 
I update OQC test log
刚开始是为了我们找不到原因，所以这情况还发生，
OQC 100% 
测试也不是效果的对策，上次两台都有
OQC 
测试但是还被这样的，来客人还发生这问题。
所以没有原因很难改善
 
 
Best Regards
---------------
Vanila_CQA Dept
Vietnam Accton Technology Co.,Ltd
 
 
 
-----Original Message-----
From: tiffany_liu 
劉玉萱
 <

>
Sent: Tuesday, May 26, 2026 3:21 PM
陈氏银
 Trần Thị Ngân <

>; henry_lee 
李逢榮
 <

>
何峻維
 <

>; kc_fan 
范光啓
 <

>; kelly 
孫惠珍
 <

>; gina_lin 
林美均
 <

>; eric1_lin 
林威廷
 <

>; benson_peng 
彭智德
 <

>; jack_chuang 
莊永豪
 <

>; cy_chao 
趙中揚
 <

>
Subject: ITUS Ticket#49530 [Vnet4624T] boot diagui
 
Remove customer
 
Hi Vanila,
 
如昨天所談，
ITUS
客戶
Vnet4624T
又新增了兩台
DOA- OS missing
連同四月的兩台，近期內已經有四台發生這樣的狀況
...
 
1.
請協助盡快調查產線
FDL
流程，是否有瑕疵
?
2.Nand Flash
是否有
quality
疑慮的紀錄
?
3.
另外也請協助提供
100% OQC
的
Log
供參考
 
 
目前看起來是
download
後斷電
(
且須持續一陣子
=
運送時間
) 
再上電
OS
就會不見
客戶提供的
log
如附件
  
謝謝
!
 
 
Best Regards,
Tiffany Liu | Engineer of Product & Quality Management Div
Email: 

 | Contact: +886 3 563 8888 
#5034
 
tiffany_liu 
劉玉萱
 (Tech Support System)
May 25, 2026, 17:54 GMT+8
Private note
<Update>
 
越南廠提供
FDL Log
如附件，確認有正確
download 
客戶
FW
目前看起來問題會在，
Download
完成後斷電放置一段時間
(
運輸到客戶端
) 
再上電，這時候就會
missing FW
 
Attachment(s)
EC03D26B100075_PASS_Y_1_015253.cap.zip
EC03D26B400081_PASS_Y_2_022700.cap (1).zip
 
tiffany_liu 
劉玉萱
 (Tech Support System)
May 25, 2026, 16:14 GMT+8
Private note
<Update>
 
客戶提供的
log
如附件
 
Attachment(s)
Vnet4624T EC03D26B100075.log
Vnet4624T EC03D26B400081.log
 
gina_lin 
林美均
 (Tech Support System)
May 25, 2026, 13:48 GMT+8
Private note
Hi Yano-san,
 
I hope this e-mail finds you well!
 
Apologies this inconvenience issue cause for you again.
Our QC have improved the load firmware issue strength the management before shipping out for you since last time. We're regret to hear this issue again.  
 
I have informed our QC team and make a ticket for this issue.
Can you help to deliver these two units back to us?
 
2026 May
S/N:EC03D26B100075
S/N:EC03D26B400081
Thank you!
 
 
Hi Tiffany, 
@tiffany_liu 
劉玉萱
 
Per our talked, please kindly confirm with factory and figure out this main issue caused.
Thank you!
 
Best Regards,
Gina Lin  
 
 
 
-----Original Message-----
From: SHINICHI YANO (
矢野真一
) <

>
Sent: Monday, May 25, 2026 12:41 PM
林美均
 <

>; kelly 
孫惠珍
 <

>

; 

Subject: [Vnet4624T] boot diagui
 
[WARNING!!] Mail from outside!!  Don’t click on links or attachments without confirmation.
*********************************************************************************
 
Dear gina and kelly,
 
How are you.
 
Recently, we have identified several 4624T units that are being excluded from our inspection process.
 
2025 Dec
S/N:EC03D25K500198
 
2026 Jan
S/N:EC03D25K200059
 
2026 May
S/N:EC03D26B100075
S/N:EC03D26B400081
 
These devices load the Diag Firmware instead of our customized firmware after booting up.
 
====These error devices====
Loading Runtime Image File : .fs/diag_ecs4130_ac5.bix
 
====Normal devices====
Loading Runtime Image File : .fs/Vnet4624T_V1.2.0.13.bix
 
Your contact person is tiffany.
 
Based on tiffany report, we have received confirmation that this issue will not occur after April 22, 2026, following a review of our Outgoing Quality Controls (OQC) .
 
However, we encountered a similar problem this month.
 
First, I have a question I'd like to ask; please answer it.
Please tell me when "OQC" will be implemented.
 
Thank you.
Bestregards,
 
--
==================================
株式会社 アイタス
・
ジャパン
ネットワーク技術部矢野 真一
(
ヤノ シンイチ
)
 
〒
103-0002
東京都中央区日本橋馬喰町
2-7-8
いちご日本橋イーストビル３階
 
Mail/teams:

Fax:
===================================
 
You are an agent. Add a comment by replying to this email or 
view ticket in Zendesk Support
.
Ticket #
49530
Status
On-hold
Requester
gina_lin 
林美均
CCs
ITUS_Junehun Kim, ITUS_Si_Yano, Sg Lee, kelly 
孫惠珍
, tiffany_liu 
劉玉萱
Followers
kc_fan 
范光啓
, kelly 
孫惠珍
, ken_tseng 
曾志鏘
, serena_hung 
洪慧純
, tiffany_liu 
劉玉萱
Group
Edgecore Quality team
Assignee
tiffany_liu 
劉玉萱
Priority
Normal
Type
Ticket
Channel
By Mail
 
This email is a service from Tech Support System.
[W13P1D-J2V12]Ticket-Id:49530Account-Subdomain:edgecore
