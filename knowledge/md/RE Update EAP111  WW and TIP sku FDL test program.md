# RE: Update EAP111  WW and TIP sku FDL test program

- Sender: ['=?utf-8?B?bWF5X3d1IOWQs+e+jueOiQ==?= <>']
- Date: Fri, 10 Apr 2026 09:18:46 +0000
- Source File: RE_ Update EAP111  WW and TIP sku FDL test program .msg

---

## ✅ Summary
Hi Wenqiang ,
有個問題
版本
R01 / R01A
是要識別新舊

---

## ✅ Clean Content
Hi Wenqiang ,
 
有個問題
版本
 R01 / R01A 
是要識別新舊
PHY ,
但是
VN
舊
PHY
都用完了無法上線驗證
-
因
ECN
導入
DCC
都要求需要驗證完成才可會簽
或是您手上還有舊
PHY
機台用線上試跑的結果來提供給
DCC
呢

 
謝謝


---

## ✅ Full Content
Hi Wenqiang ,
 
有個問題
版本
 R01 / R01A 
是要識別新舊
PHY ,
但是
VN
舊
PHY
都用完了，無法上線驗證
-
因
ECN
導入
DCC
都要求需要驗證完成才可會簽
或是您手上還有舊
PHY
機台，用線上試跑的結果來提供給
DCC
呢
?
 
謝謝
!!
 
 
 
 
From:
 wenqiang_zhang 
张文强
 <> 
Sent:
 Wednesday, April 8, 2026 5:26 PM
 alex_chiang 
江育誠
 <>; ck_yang 
楊智凱
 <>; azhu_kang 
阿朱
 <>
 may_wu 
吳美玉
 <>; kentchiou 
邱福壽
 <>; simon_kang 
康信雄
 <>
Subject:
 
回复
: Update EAP111 WW and TIP sku FDL test program 
 
Hi May
：
还请帮忙确认是否需要切入
ECN
把新的版本导入
Bom
，谢谢！
 
 
 
Best regards,
ATVN WenQiang
 
发件人
:
 alex_chiang 
江育誠
 <

> 
发送时间
:
 2026
年
4
月
8
日
 13:04
收件人
:
 ck_yang 
楊智凱
 <

>; azhu_kang 
阿朱
 <

>
抄送
:
 wenqiang_zhang 
张文强
 <

>; may_wu 
吳美玉
 <

>; kentchiou 
邱福壽
 <

>; simon_kang 
康信雄
 <

>
主题
:
 
回覆
: Update EAP111 WW and TIP sku FDL test program 
 
Ｈ
i Azhu,
 
Test Program Version: V12.4.91-796.1F.4.5 
Test Program Version: V4.1.1.1F.5.1
檢查結果，
LOG
內容符合預期，並無異常，謝謝
 
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
8
日
 
下午
 01:43
收件者
:
 azhu_kang 
阿朱
 <

>; alex_chiang 
江育誠
 <

>
:
 wenqiang_zhang 
张文强
 <

>; may_wu 
吳美玉
 <

>; kentchiou 
邱福壽
 <

>; simon_kang 
康信雄
 <

>
主旨
:
 
回覆
: Update EAP111 WW and TIP sku FDL test program 
 
Hi Azhu:
                  Log OK, 
麻煩
Alex 
抽空確認一下
 
Best Regards
CK
寄件者
:
 azhu_kang 
阿朱
 <

>
寄件日期
:
 2026
年
4
月
8
日
 
下午
 12:07
收件者
:
 ck_yang 
楊智凱
 <

>; alex_chiang 
江育誠
 <

>
:
 wenqiang_zhang 
张文强
 <

>; may_wu 
吳美玉
 <

>; kentchiou 
邱福壽
 <

>; simon_kang 
康信雄
 <

>
主旨
:
 RE: Update EAP111 WW and TIP sku FDL test program 
 
Hi CK and Alex;
 
         
附件是
log file FDL EAP111(TIP), EAP111(WW)
，请确认一下，谢谢
Ex
：
TIP_EC_PASS_N_1_104349 
EAP111-0223-WL_V4.1.1.1F.5.1_FDL.7z
​
WW_EC_PASS_N_1_105013 
​
EAP111-0223-WL_V12.4.91-796.1F.4.5_FDL.zip
​
 
Regards, thanks
ATVN Azhu_kang, PE Dept.  #VD2900
 
From:
 ck_yang 
楊智凱
 <

> 
Sent:
 Tuesday, April 7, 2026 3:05 PM
 wenqiang_zhang 
张文强
 <

>; azhu_kang 
阿朱
 <

>
 may_wu 
吳美玉
 <

>; kentchiou 
邱福壽
 <

>; simon_kang 
康信雄
 <

>; alex_chiang 
江育誠
 <

>
Subject:
 Update EAP111 WW and TIP sku FDL test program 
 
Hi 
文強
 and 
阿朱
:
               
請更新
EAP111 WW and TIP FDL 
站使用產測程式
:
    
WW Link:
           
​
EAP111-0223-WL_V12.4.91-796.1F.4.5_FDL.zip
​
TIP Link:
                     
​
EAP111-0223-WL_V4.1.1.1F.5.1_FDL.7z
​
 
       
主要修改說明
:
             
最近於
Ericsson 
專案中發現由於有機率多出現點
. 
導致產測抓取
hw version 
多抓到點
.
             
因此產測進行修改
                 
錯誤抓取
                    
                
                
正確抓取
:
                      
 
以上產測版本
,
越南的
MT151 
已經開啟
請驗證產測完畢
,
麻煩請寄
PASS log 
請
SW  Alex_Chiang  
再次進行確認
 
Best Regards
CK
