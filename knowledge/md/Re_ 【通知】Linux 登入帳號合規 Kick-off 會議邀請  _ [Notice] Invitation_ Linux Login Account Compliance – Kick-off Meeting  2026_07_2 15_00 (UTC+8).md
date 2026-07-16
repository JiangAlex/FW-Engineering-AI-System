# Re: 【通知】Linux 登入帳號合規 Kick-off 會議邀請  | [Notice] Invitation: Linux Login Account Compliance – Kick-off Meeting  2026/07/2 15:00 (UTC+8)

- Sender: 
- Date: 
- Source File: Re_ 【通知】Linux 登入帳號合規 Kick-off 會議邀請  _ [Notice] Invitation_ Linux Login Account Compliance – Kick-off Meeting  2026_07_2 15_00 (UTC+8).msg

---

## ✅ Summary
Hi  CK
你先參考一下我會𣏾你討論
取得
iOS 版 Outlook
寄件者:

---

## ✅ Clean Content
Hi  CK



你先參考一下我會𣏾你討論














取得

iOS 版 Outlook




寄件者:
 friday_hung 洪郡祥 


寄件日期:
 Wednesday, 08 July 2026 18:12:10


收件者:
 lanqly_chou 周偉堯  alex_chiang 江育誠 


主旨:
 RE: 通知Linux 登入帳號合規 Kick-off 會議邀請  Notice Invitation: Linux Login Account Compliance  Kick-off Meeting 2026/07/2 15:00 (UTC8)


 










Hi 


@alex_chiang 


江育誠


 


以下我提供目前各個區域
VM
透過
API
存取憑證的方式


竹南


curl -k -fsS -O 
https://openwificert.accton.com.tw/1/generated/4445BA42F061.tar.gz


 


竹北


curl -k -fsS -O 

https://openwificertzb.accton.com/1/generated/D077CE69E57C.tar.gz


 


越南


curl -k -fsS --noproxy  -O 
https://10.150.192.41/1/generated/4445BA42F061.tar.gz


 


竹南竹北我有請
MIS rice
幫我測試過產線是否能通


 


再麻煩你也幫忙測試看看


 


 


Regards,


Friday

---

## ✅ Full Content
Hi  CK



你先參考一下，我會𣏾你討論。














取得

iOS 版 Outlook




寄件者:
 friday_hung 洪郡祥 <>


寄件日期:
 Wednesday, 08 July 2026 18:12:10


收件者:
 lanqly_chou 周偉堯 <>; alex_chiang 江育誠 <>


主旨:
 RE: 【通知】Linux 登入帳號合規 Kick-off 會議邀請 | [Notice] Invitation: Linux Login Account Compliance – Kick-off Meeting 2026/07/2 15:00 (UTC+8)


 










Hi 


@alex_chiang 


江育誠


 


以下我提供目前各個區域
VM
透過
API
存取憑證的方式


竹南


curl -k -fsS -O "
https://openwificert.accton.com.tw/1/generated/4445BA42F061.tar.gz"


 


竹北


curl -k -fsS -O 

https://openwificertzb.accton.com/1/generated/D077CE69E57C.tar.gz


 


越南


curl -k -fsS --noproxy '*' -O "
https://10.150.192.41/1/generated/4445BA42F061.tar.gz"


 


竹南竹北我有請
MIS rice
幫我測試過產線是否能通


 


再麻煩你也幫忙測試看看


 


 


Regards,


Friday


 






From:
 shaun_chuang

莊政煊
 <>



Sent:
 Tuesday, July 7, 2026 3:38 PM


 friday_hung 
洪郡祥
 <>; lanqly_chou

周偉堯
 <>


 alex_chiang 
江育誠
 <>; ted_yu

余淳驊
 <>; mika_liang

梁思婷
 <>


Subject:
 RE: 
【通知】
Linux

登入帳號合規
 Kick-off

會議邀請
 | [Notice] Invitation: Linux Login Account Compliance – Kick-off Meeting 2026/07/2 15:00 (UTC+8)






 


Hi Friday,


 


經討論


我仍然會按照原本計畫進行部署，


部署後
90
天內須更換密碼，


API
的方式如果來不及完成，


則不更換密碼，提供指令展延既有密碼


 


API
存取的方式完成後關閉不再使用的
linux
帳號


您再提供
API
存取的方式預計完成時間


 


謝謝


 


 




Best Regards,

Shaun Chuang


 


Platform Management Dept.


Infrastructure and Platform Mgmt. Div.


Accton Technology Corp.




E-mail
：





 






From:
 shaun_chuang

莊政煊




Sent:
 Tuesday, July 7, 2026 11:29 AM


 friday_hung 
洪郡祥
 <

>; lanqly_chou

周偉堯
 <

>


 alex_chiang 
江育誠
 <

>; ted_yu

余淳驊
 <

>; mika_liang

梁思婷
 <

>


Subject:
 RE: 
【通知】
Linux

登入帳號合規


Kick-off 
會議邀請
 | [Notice] Invitation: Linux Login Account Compliance – Kick-off Meeting
 2026/07/2 15:00 (UTC+8)






 


Loop Ted, Mika


 




Best Regards,

Shaun Chuang


 


Platform Management Dept.


Infrastructure and Platform Mgmt. Div.


Accton Technology Corp.




E-mail
：





 






From:
 friday_hung

洪郡祥
 <

>



Sent:
 Tuesday, July 7, 2026 10:42 AM


 shaun_chuang 
莊政煊
 <

>; lanqly_chou

周偉堯
 <

>


 alex_chiang 
江育誠
 <

>


Subject:
 RE: 
【通知】
Linux

登入帳號合規
 Kick-off

會議邀請
 | [Notice] Invitation: Linux Login Account Compliance – Kick-off Meeting 2026/07/2 15:00 (UTC+8)






 


Hi 


@lanqly_chou 


周偉堯


 


目前
MIS
針對工廠的
server
有新的配置
,

如附件


 


我跟
MIS
討論後
,

跟我們相關的部分是要避免產測
login
到工廠
server


 


而產線的站台改透過
API
的方式去存取工廠
server
的檔案是可以接受的


 


MIS
的時限是設定在
8/31
後必須要更換密碼
,

但我們的生產並沒辦法在
8/31
將所有設備的產測都做更換


 


更換密碼的時間要再跟
  
@shaun_chuang

莊政煊


討論看看


 


我這邊則一邊確認竹南
/
竹北
/
越南的
API
狀況


 


 


Regards,


Friday


 




-----Original Appointment-----


From:
 shaun_chuang 
莊政煊
 <

>



Sent:
 Thursday, June 25, 2026 3:37 PM


 erik_hsu 
許彧嘉
; hank18_wang

王裕涵
; mika_liang

梁思婷
; bird_chiu

邱惠傑
; brian_yang

楊順翔
; tyler_nguyen

阮文秀
 Nguyễn Văn Tú; friday_hung

洪郡祥
; bagel_ku

古貝宣
; dong_xiong

熊冬
; gordon_nguyen

阮英山
; lifei_ye

叶李飞
; shaun_chuang

莊政煊
; jerry_ke

柯翊偉
; anita_zhu

朱依純
; russo_sung

宋柏翰
; lancia_chen

陳祈瑋
; ninlun_li

李旻倫
; yunsheng_chen

陳昀昇
; taylor_hsu

徐浦濬
; rice_chang

張允誠
; rob_lin

林昱廷
; nuo_kuo

郭芃成
; natalie_shen

沈寀捷
; nikki_chen

陳聰穎
; haowei_wang

王皓維
; ron_tseng

曾致融
; ted_yu

余淳驊
; alan_lin

林裕鈞
; jena_wu

吳珈禎
; #MISC_CS_CSD; lion_lee

黎猛
; joseph_liu

劉曦
; caro

余佳穎
; #MISC_IPM_SSD_NRMS; #MISC_IPM_SSD_SAS


Subject:
 
【通知】
Linux

登入帳號合規
 Kick-off

會議邀請
 | [Notice] Invitation: Linux Login Account Compliance – Kick-off Meeting 2026/07/2 15:00 (UTC+8)


When:
 2026
年
7
月
2
日星期四


下午


03:00-
下午
 03:30 (UTC+08:00)

台北。


Where:
 Microsoft Teams 
會議




 


Hi All,


 


為確保
 Linux server

帳號密碼規範符合
 ISMS

與資安要求，將進行
 Linux

密碼複雜度設定。


To ensure that Linux server account password policies comply with ISMS and information security requirements, Linux password complexity settings will be updated.


 


Kick-off meeting 
將於
 2026/07/02 15:00 (UTC+8)

舉行，會中將說明相關注意事項。


The kick-off meeting will be held on 2026/07/02 at 15:00 (UTC+8), during which the related precautions and details will be explained.


 


Site
：
ZB / ZN / VN


Linux OS scope
：
Ubuntu + Red Hat


 


套用範圍：
Linux

使用者登入帳號


Scope: Linux user login accounts


 


不包含服務帳號，服務帳號不受本次密碼過期策略影響。


Service accounts are excluded and are not affected by this password expiration policy.


 






Password rules will be changed as follows:


密碼規則將更改為以下：




密碼長度：需
 18

字元以上

Password length: Must be at least 18 characters
密碼複雜度：需包含英文大寫、小寫、數字、符號
 4

種

Password complexity: Must include 4 character types: uppercase letters, lowercase letters, numbers, and symbols
歷史密碼限制：請勿與前
 10

組密碼相同

Password history restriction: The password must not be the same as the previous 10 passwords
更換週期：密碼每
 90

天需更改一次

Password change cycle: Passwords must be changed every 90 days
更換限制：密碼
 1

天內僅能變更一次

Password change restriction: Passwords can only be changed once per day
錯誤登入鎖定：

Account lockout policy:






嘗試錯誤登入
 5

次後鎖定帳號

The account will be locked after 5 invalid login attempts
鎖定時間為
 15

分鐘

The lockout duration is 15 minutes




________________________________________________________________________________






Microsoft Teams

會議








加入
:

https://teams.microsoft.com/meet/?p=FHvDxN2XQtqEs73z3a








會議識別碼
:

 26








密碼
:

SY2jA77F


















需要協助嗎
?


|




系統參考










透過電話撥入








+886 2 7752 4356,,#


台灣
,

信義區








尋找當地號碼










電話會議識別碼
:

#








針對召集人
:

會議選項


|




重設撥入
 PIN

碼








________________________________________________________________________________
