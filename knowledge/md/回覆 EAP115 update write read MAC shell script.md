# 回覆: EAP115 update write read MAC shell script

- Sender: ['=?utf-8?B?Y2tfeWFuZyDmpYrmmbrlh7E=?= <>']
- Date: Tue, 28 Apr 2026 06:16:10 +0000
- Source File: 回覆_ EAP115 update write read MAC shell script.msg

---

## ✅ Summary
Hi Saoan:
那個有跑完整PT 測試包含RF 測試剛好越南產線沒再使用,借用越南產線跑的
新竹這邊要跑Power Cycle 測試需要忽略RF 部分(Itest YC 使用中)
Best Regards
CK

---

## ✅ Clean Content
Hi Saoan:



           那個有跑完整PT 測試包含RF 測試剛好越南產線沒再使用,借用越南產線跑的



           新竹這邊要跑Power Cycle 測試需要忽略RF 部分(Itest YC 使用中)









Best Regards



CK






寄件者:
 saoan_ho 何紹安 


寄件日期:
 2026年4月28日 下午 01:58


收件者:
 ck_yang 楊智凱  julie_lin 林季蓉 


 brandon_wu 吳諭旻  alex_chiang 江育誠  jeter_lai 賴奇郁  victor_tsai 蔡文人  jason_yu 余建雄 


主旨:
 RE: EAP115 update write read MAC shell script


 










HI CK,


我看那兩次
Fail

一次是在第一次開機時沒有中斷到導致一直開機到
kernel.


另一次是在最後一次重開機時也沒中斷到也是一直開機到
kernel.


其他好像沒有什麼問題
.


 


晚點我可以再拿另一片換過
DDR
和
NAND
的板子給您跑
Power cycle
嗎



 


Best Regards

Accton Technology Corp. Taipei

Tel: 886-


10694 
台北市大安區光復南路
102
號
13
樓


何紹安




---

## ✅ Full Content
Hi Saoan:



           那個有跑完整PT 測試包含RF 測試剛好越南產線沒再使用,借用越南產線跑的



           新竹這邊要跑Power Cycle 測試需要忽略RF 部分(Itest YC 使用中)









Best Regards



CK






寄件者:
 saoan_ho 何紹安 <>


寄件日期:
 2026年4月28日 下午 01:58


收件者:
 ck_yang 楊智凱 <>; julie_lin 林季蓉 <>


 brandon_wu 吳諭旻 <>; alex_chiang 江育誠 <>; jeter_lai 賴奇郁 <>; victor_tsai 蔡文人 <>; jason_yu 余建雄 <>


主旨:
 RE: EAP115 update write read MAC shell script


 










HI CK,


我看那兩次
Fail

一次是在第一次開機時沒有中斷到導致一直開機到
kernel.


另一次是在最後一次重開機時也沒中斷到也是一直開機到
kernel.


其他好像沒有什麼問題
.


 


晚點我可以再拿另一片換過
DDR
和
NAND
的板子給您跑
Power cycle
嗎
?


 


Best Regards

Accton Technology Corp. Taipei

Tel: 886-2-8773-8500#1018


10694 
台北市大安區光復南路
102
號
13
樓


何紹安





 


 






From:
 ck_yang

楊智凱
 <>



Sent:
 Tuesday, April 28, 2026 1:32 PM


 saoan_ho 
何紹安
 <>; julie_lin

林季蓉
 <>


 brandon_wu 
吳諭旻
 <>; alex_chiang

江育誠
 <>; jeter_lai

賴奇郁
 <>; victor_tsai

蔡文人
 <>; jason_yu

余建雄
 <>


Subject:
 
回覆
: EAP115 update write read MAC shell script






 




Hi All:






           

更新一下






           

目前
PT

使用新流程跑壓力測試近
200
次
,
其中有兩次無成功進到
uboot
 FAIL 
外其餘測試皆
pass






 






 






Best Regards






CK












寄件者
:

 saoan_ho 
何紹安
 <

>


寄件日期
:

 2026
年
4
月
24
日


下午
 05:25


收件者
:

 ck_yang 
楊智凱
 <

>; julie_lin

林季蓉
 <

>


:

 brandon_wu 
吳諭旻
 <

>; alex_chiang

江育誠
 <

>; jeter_lai

賴奇郁
 <

>; victor_tsai

蔡文人
 <

>; jason_yu

余建雄
 <

>


主旨
:

 RE: EAP115 update write read MAC shell script
 




 










Hi CK,


這樣的話
,



看能不能做
PT
時
USB
測
A
面


FDL
再測
B
面
(
用同一種
dongle

做
A/B
面記號
)


 


Best Regards

Accton Technology Corp. Taipei

Tel: 886-2-8773-8500#1018


10694 
台北市大安區光復南路
102
號
13
樓


何紹安





 


 






From:
 ck_yang

楊智凱
 <

>



Sent:
 Friday, April 24, 2026 5:18 PM


 julie_lin 
林季蓉
 <

>


 brandon_wu 
吳諭旻
 <

>; saoan_ho

何紹安
 <

>; alex_chiang

江育誠
 <

>; jeter_lai

賴奇郁
 <

>; victor_tsai

蔡文人
 <

>; jason_yu

余建雄
 <

>


Subject:
 
回覆
: EAP115 update write read MAC shell script






 




Hi Julie:






             






               
關於
(3)
項目
,
剛了解一下
:






               
原本
FDL

由
type -c

供電進行測試
,
如改測
USB dongle 
後
,
須一開始
FDL

測試就使用
POE
供電






               
實際找
USB

插入
(
如下圖
)
因為治具空間有限
,
如
USB
 dongle 
先固定治具上
,
等待
DUT
推入後再插入
USB
 dongle






               
可能測試單面
USB dongle,
測試過程中要拔插換面測試有難度






               
這可能再找
CC
魏逸民討論






 






 






 






 
         






 






 






 












 






 






Best Regards






CK






 












寄件者
:

 victor_tsai 
蔡文人
 <

>


寄件日期
:

 2026
年
4
月
24
日


下午
 02:17


收件者
:

 ck_yang 
楊智凱
 <

>; jason_yu

余建雄
 <

>; julie_lin

林季蓉
 <

>


:

 brandon_wu 
吳諭旻
 <

>; saoan_ho

何紹安
 <

>; alex_chiang

江育誠
 <

>; jeter_lai

賴奇郁
 <

>


主旨
:


回覆
: EAP115 update write read MAC shell script






 










Hi CK,






 






MAC

部分


看起來流程
OK












寄件者
:

 ck_yang 
楊智凱
 <

>


寄件日期
:

 2026
年
4
月
24
日


下午
 01:48


收件者
:

 jason_yu 
余建雄
 <

>; victor_tsai

蔡文人
 <

>; julie_lin

林季蓉
 <

>


:

 brandon_wu 
吳諭旻
 <

>; saoan_ho

何紹安
 <

>; alex_chiang

江育誠
 <

>; jeter_lai

賴奇郁
 <

>


主旨
:


回覆
: EAP115 update write read MAC shell script






 










Hi Jason and Victor:






         

了解
,

已修改了
,

請再確認附檔
log
內容符合你們需求
?






 






Best Regards






CK






           






 












寄件者
:

 jason_yu 
余建雄
 <

>


寄件日期
:

 2026
年
4
月
24
日


上午
 10:07


收件者
:

 ck_yang 
楊智凱
 <

>; victor_tsai

蔡文人
 <

>; julie_lin

林季蓉
 <

>


:

 brandon_wu 
吳諭旻
 <

>; saoan_ho

何紹安
 <

>; alex_chiang

江育誠
 <

>; jeter_lai

賴奇郁
 <

>


主旨
:

 RE: EAP115 update write read MAC shell script
 




 










Hi CK,


 


為了能更清楚的看到問題，可否在
 WDT reboot

之前再次用


sh /etc/Accton/mtk_factory_tool.sh read


來確認一下
 SN/MAC

是否還存在。


 


Regards,


Jason






From:
 ck_yang

楊智凱
 <

>



Sent:
 Thursday, April 23, 2026 5:16 PM


 victor_tsai 
蔡文人
 <

>; julie_lin

林季蓉
 <

>


 brandon_wu 
吳諭旻
 <

>; jason_yu

余建雄
 <

>; saoan_ho

何紹安
 <

>; alex_chiang

江育誠
 <

>; jeter_lai

賴奇郁
 <

>


Subject:
 
回覆
: EAP115 update write read MAC shell script






 




Hi All:






             
附檔新修改後重跑
EAP115  PT test log,
請確認內容流程是否正確
?






             
主要修改以下
:






                          1.
增加以下指令






1.
       

hexdump -C -s 0x1324 -n 1 /lib/firmware/e2p








                                                 

i.hexdump -C -s 0x1336 -n 1 /lib/firmware/e2p






                           2. Write mac

增加指令






                                     
jffs2reset -y






                          3.
使用新的
write mac script
 : 






                                     

 mtk_factory_tool.sh






              






 






Best Regards






CK














寄件者
:
 victor_tsai

蔡文人
 <

>


寄件日期
:
 2026
年
4
月
22
日


上午
 09:22


收件者
:
 julie_lin

林季蓉
 <

>; ck_yang

楊智凱
 <

>


:
 brandon_wu

吳諭旻
 <

>; jason_yu

余建雄
 <

>; saoan_ho

何紹安
 <

>; alex_chiang

江育誠
 <

>; jeter_lai

賴奇郁
 <

>


主旨
:
 
回覆
:
 EAP115 update write read MAC shell script






 








Hi CK,






 






TRD

請參考
 
​
EAP115_v0.
​






 






EAP115_Funtion_Test_Items_version_v0.3.2_.doc






 






Victor






 














寄件者
:
 julie_lin

林季蓉
 <

>


寄件日期
:
 2026
年
4
月
22
日


上午
 08:20


收件者
:
 ck_yang

楊智凱
 <

>; victor_tsai

蔡文人
 <

>


:
 brandon_wu

吳諭旻
 <

>; jason_yu

余建雄
 <

>; saoan_ho

何紹安
 <

>; alex_chiang

江育誠
 <

>; jeter_lai

賴奇郁
 <

>


主旨
:
 RE:
 EAP115 update write read MAC shell script






 






Hi CK,


本週
HW

稍微看過
log,

此次第一套生產的
200pcs check mac issue
的發生機率為
2%,

接續的
400+400pcs
則發生一次


下次生產請幫忙導入
:


 


(1)

尚未加入的
command


>
執行


jffs2reset -y
  

清除所有暫存檔


>
做
 WDT
 reboot


(2)

Brandon
以下建議的流程


(3) FDL
加測
USB dongle (
流程先前討論為
:
 POE
上電
->

插
USB dongle
測
 ->
 POE
斷電
 -> USB-C
供電
 ->
 Download AP code)


 


下一次預計
5/6
投產
,

請再評估一下時間
,

如有問題再討論
,

謝謝
!


(1) EAP115a (TE): 4200pcs


(2) EAP115 (T): 50pcs


 


Hi Victor,


提供給產測的流程及作法請務必更新到
TRD
上
,

謝謝


 


 


BR,


Julie


 


Ext.: 3167



PM - Accton Tech. Corp.


 




From:
 brandon_wu

吳諭旻
 <

>


Sent:
 Tuesday, April 21, 2026 2:33 PM


 ck_yang 
楊智凱
 <

>; jason_yu

余建雄
 <

>; victor_tsai

蔡文人
 <

>; saoan_ho

何紹安
 <

>; julie_lin

林季蓉
 <

>; alex_chiang

江育誠
 <

>; jeter_lai

賴奇郁
 <

>


Subject:
 RE: EAP115 update write read MAC shell script




 


Hi CK,


 


產測再麻煩協助加入此程序
.


在做
WiFi Test 
之前先分別下兩段
command.
如同
RF
測試完後
 2G & 5G Cal Data Check
的動作
.




hexdump -C -s 0x1324 -n 1 /lib/firmware/e2p
hexdump -C -s 0x1336 -n 1 /lib/firmware/e2p


在
RF Test
前下此
command
分別會是
Brd File Default
值
C5 

以及
 C3. 


 


主要是確保 後續
Cal
完有正確寫入
Cal Data.


 


 


 


Thanks.


BRs,


Brandon.


Accton Technology Crop. Taipei


Tel:886-2-8873-8500#1085



10694
台北市大安區光復南路
102
號
13
樓


吳諭旻





 




From:
 ck_yang

楊智凱
 <

>


Sent:
 Tuesday, April 14, 2026 10:43 AM


 jason_yu 
余建雄
 <

>; victor_tsai

蔡文人
 <

>; brandon_wu

吳諭旻
 <

>; saoan_ho

何紹安
 <

>; julie_lin

林季蓉
 <

>; alex_chiang

江育誠
 <

>


Subject:
 
回覆
: EAP115 update write read MAC shell script




 


Please mail loop "PM" "HW" "Alex_Chiang"


 


Hi Victor:


               
以上變更是否有要更新到
TRD
文件內容
?


 


 


Best Regards


CK










寄件者
:
 jason_yu

余建雄
 <

>


寄件日期
:
 2026
年
4
月
14
日


上午
 10:01


收件者
:
 victor_tsai

蔡文人
 <

>;
 ck_yang 
楊智凱
 <

>


主旨
:
 RE:
 EAP115 update write read MAC shell script


 




Hi CK,


 


我再說明一下，順序是這樣，


 


寫
SN/MAC


檢查
 SN/MAC


做其他的測試
 LED, Ethernet….


在做
 WDT reboot

之前，再做一次讀取
 SN/MAC

來確認在我們
 reboot 

之前
 MAC 
的狀態


執行
 


jffs2reset -y
  

清除所有暫存檔


做
 WDT reboot


 


Regards,


Jason




From:
 victor_tsai

蔡文人
 <

>


Sent:
 Tuesday, April 14, 2026 9:53 AM


 ck_yang 
楊智凱
 <

>


 jason_yu 
余建雄
 <

>


Subject:
 EAP115 update write read MAC shell script




 


Hi CK,


 


我幫你整理出
 command

跟
 log (
紅色部分
), 

增加了一行
 (
jffs2reset -y
)
 , 
再啟動
watchdog

之前
.

如有問題再討論
.


 


/*kernel write read command*/


cd /etc/Accton


tftp -g -r mtk_factory_tool.sh 192.168.1.10


chmod +x /etc/Accton/mtk_factory_tool.sh


sh /etc/Accton/mtk_factory_tool.sh --sn SN_ --mode MOD_ --hwver HW_ --mac 90:11:22:33:44:55


sh /etc/Accton/mtk_factory_tool.sh read


jffs2reset -y


kill $(pidof sh /etc/Accton/wdt_esd_touch_timeout.sh)


 


/* uboot read mac command*/


 


mtd read factory 0x 0x0 0x2000


md.b 0x 0x6


md.b 0x4600000a 0x6


md.b 0x 0x20


md.b 0x 0x20


md.b 0x460000a0 0x20


md.b 0x 0x2


md.b 0x 0x2


mtd read factory 0x 0xFF800 0x800


md.b 0x460007f4 0x6


md.b 0x460007fa 0x6


 


/* test log message*/


root@TestMode:/#

cd /etc/Accton


root@TestMode:/etc/Accton#

tftp -g -r mtk_factory_tool.sh 192.168.1.10


root@TestMode:/etc/Accton#

chmod +x /etc/Accton/mtk_factory_tool.sh


root@TestMode:/etc/Accton#

sh /etc/Accton/mtk_factory_tool.sh --sn SN_


30 --mode MOD_ --hwver HW_ --mac 90:11:22:33:44:55


[INIT] MediaTek Factory Tool v0.1


Pre-cleaning E2P file: /lib/firmware/e2p


[INFO] Committing to Factory...


Unlocking Factory ...


 


Writing from /tmp/Factory.batch to Factory ...


[INFO] Verifying Flash Integrity...


[INFO] MD5 Checksum Match: d8814d1d4f18e66eeea


[INFO] E2P cache invalidated and filesystem synced.


[SUCCESS] All tasks completed.


root@TestMode:/etc/Accton#

sh /etc/Accton/mtk_factory_tool.sh read


[INIT] MediaTek Factory Tool v0.1


--- Current Factory Data ---


Serial    (0x60)   : SN_


Mode      (0x80)   : MOD_


Hardware  (0xA0)   : HW_


WAN MAC   (0xFFFFA): 90:11:22:33:44:55


LAN MAC   (0xFFFF4): 90:11:22:33:44:56


WiFi1 MAC (0x04)   : 90:11:22:33:44:57


WiFi2 MAC (0x0A)   : 90:11:22:33:44:58


root@TestMode:/etc/Accton#

jffs2reset -y


/dev/ubi0_2 is mounted as /overlay, only erasing files


root@TestMode:/etc/Accton#

kill $(pidof sh /etc/Accton/wdt_esd_touch_timeout.sh)


root@TestMode:/etc/Accton#


F0: 102B 0000


F9: 1042 0000


F9: 1042 0000 [0200]


F8: 0000 0000


V0: 0000 0000 [0001]


00: 0000 0000


BP: 0680 0041 [0000]


G0: 1190 0000


EC: 0000 0000 [2000]


MK: 0000 0000 [0000]


T0: 0000 0385 [0101]


Jump to BL


 


 


MT7987>

mtd read factory 0x 0x0 0x2000


Reading 8192 byte(s) at offset 0x


MT7987>

md.b 0x 0x6


: 90 11 22 33 44 57                                .."3DW


MT7987>

md.b 0x4600000a 0x6


4600000a: 90 11 22 33 44 58                                .."3DX


MT7987>

md.b 0x 0x20


: 53 4e 5f 32 30 32 36 30 34 31 34 30 39 33 30 00  SN_.


: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................


MT7987>

md.b 0x 0x20


: 4d 4f 44 5f 32 30 32 36 30 34 31 34 30 39 33 30  MOD_


: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................


MT7987>

md.b 0x460000a0 0x20


460000a0: 48 57 5f 32 30 32 36 30 34 31 34 30 39 33 30 00  HW_.


460000b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................


MT7987>

md.b 0x 0x2


: c5 00                                            ..


MT7987>

md.b 0x 0x2


: c3 00                                            ..


MT7987>

mtd read factory 0x 0xFF800 0x800


Reading 2048 byte(s) at offset 0x000ff800


MT7987>

md.b 0x460007f4 0x6


460007f4: 90 11 22 33 44 56                                .."3DV


MT7987>

md.b 0x460007fa 0x6


460007fa: 90 11 22 33 44 55                                .."3DU


MT7987>
