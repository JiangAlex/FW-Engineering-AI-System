# 轉寄: EAP111 FT Calibration Data Exist Fail

- Sender: ['=?utf-8?B?Y2tfeWFuZyDmpYrmmbrlh7E=?= <ck_yang@accton.com>']
- Date: Mon, 29 Jun 2026 07:29:49 +0000
- Source File: 轉寄_ EAP111 FT Calibration Data Exist Fail.msg

---

## ✅ Summary
Mail loop add  Vince
Hi Jason:
剛剛與Vince確認後發現之前一個機制:
如果Calibration後如 5G RX marge fail 就會過程中更新brd 檔案重測,因為
/lib/firmware/MT7981_iPAiLNA_EEPROM.bin

---

## ✅ Clean Content
Mail loop add  Vince









Hi Jason:


                剛剛與Vince確認後發現之前一個機制:




                 如果Calibration後如 5G RX marge fail 就會過程中更新brd 檔案重測,因為
/lib/firmware/MT7981_iPAiLNA_EEPROM.bin
 就跟原本燒錄時不同


                產測會改檢查brd 檔案 check sum,這次FT沒有檢查brd
 檔案check sum因此判fail,現在修補起來















Hi Kent:



            以下PT/FT 產測進版



           


EAP111-0223-WL_V1.1.1F.8.3_MAIN.7z





             MT 151進版





















Best Regards



CK








寄件者:
 jason_yu 余建雄 


寄件日期:
 2026年6月29日 下午 02:33


收件者:
 ck_yang 楊智凱  victor_tsai 蔡文人 


 kentchiou 邱福壽  simon_kang 康信雄  kt_li 李坤泰  alex_chiang 江育誠  may_wu 吳美玉 


主旨:
 RE: EAP111 FT Calibration Data Exist Fail


 




Victor

---

## ✅ Full Content
Mail loop add  "Vince"









Hi Jason:


                剛剛與Vince確認後發現之前一個機制:




                 如果Calibration後如 5G RX marge fail 就會過程中更新brd 檔案重測,因為
/lib/firmware/MT7981_iPAiLNA_EEPROM.bin
 就跟原本燒錄時不同


                產測會改檢查brd 檔案 check sum,這次FT沒有檢查brd
 檔案check sum因此判fail,現在修補起來















Hi Kent:



            以下PT/FT 產測進版



           
​
​
EAP111-0223-WL_V1.1.1F.8.3_MAIN.7z
​
​



             MT 151進版





















Best Regards



CK








寄件者:
 jason_yu 余建雄 <>


寄件日期:
 2026年6月29日 下午 02:33


收件者:
 ck_yang 楊智凱 <>; victor_tsai 蔡文人 <>


 kentchiou 邱福壽 <>; simon_kang 康信雄 <>; kt_li 李坤泰 <>; alex_chiang 江育誠 <>; may_wu 吳美玉 <>


主旨:
 RE: EAP111 FT Calibration Data Exist Fail


 




+Victor


 




From:
 ck_yang

楊智凱
 <>


Sent:
 Monday, June 29, 2026 1:59 PM


 jason_yu 
余建雄
 <>


 kentchiou 
邱福壽
 <>; simon_kang

康信雄
 <>; kt_li

李坤泰
 <>; alex_chiang

江育誠
 <>; may_wu

吳美玉
 <>


Subject:
 EAP111 FT Calibration Data Exist Fail




 


Hi Jason:


               EAP111 PE
福壽反應
:


               
竹南生產
EAP111

這台在
PT
雖然幾次都
FAIL

但最後測試
PASS,
進到
FT


               
但是
FT

都在這
/lib/firmware/MT7981_iPAiLNA_EEPROM.bin: FAILED

都一直
FAIL


               
請參閱附檔
PT & FT

所有
test log


 


 


 




 


 


Best Regards


CK
