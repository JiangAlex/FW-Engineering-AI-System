# RE: OQC phy ic version fail issue

- Sender: ['=?utf-8?B?bHVuZyDlkLPlpoLns6c=?= <lung@accton.com>']
- Date: Thu, 9 Jul 2026 06:23:47 +0000
- Source File: RE_ OQC phy ic version fail issue.msg

---

## ✅ Summary
Dear May :
如剛才討論的結論
,
RI
應該在台灣開

---

## ✅ Clean Content
Dear May :
          
如剛才討論的結論
,
 RI 
應該在台灣開
, 
工單是開印度線的工單
.

---

## ✅ Full Content
Dear May :
          
如剛才討論的結論
,
 RI 
應該在台灣開
, 
工單是開印度線的工單
. 
 
From:
 may_wu 
吳美玉
 <> 
Sent:
 Monday, June 29, 2026 6:19 PM
 wendy_chiu 
邱宇絃
 <>; lung 
吳如糧
 <>
 alex_chiang 
江育誠
 <>; wii_lin 
林偉能
 <>; ck_yang 
楊智凱
 <>; rossi_chen 
陳旭
 <>; calvin_chen 
陳漢鍾
 <>; mareedu_rao Mareedu Chiranjeevi <>; sebastian_huang 
黃胤誠
 <>; lanqly_chou 
周偉堯
 <>; spoo_wei 
魏墉伸
 <>; simon_kang 
康信雄
 <>; bill_chen 
陳奕廷
 <>; austin_chang 
張金鐘
 <>; victor_wang 
王紹誠
 <>; Ashok Pal <>; Shivangi Sujal <>; Kajal Thakur <>; ravi_kant Ravi Kant <>; peifang_hung 
洪珮芳
 <>; enco 
劉升順
 <>; kentchiou 
邱福壽
 <>; alyssa_fan 
范秀景
 <>; kelsey_tsai 
蔡易儒
 <>; femehring_langhu Femehring Langhu <>; alyssa_fan 
范秀景
 <>
Subject:
 RE: OQC phy ic version fail issue
 
Hi Wendy ,
請協助會簽
 : ECN
 
80.DCC
•Description
EAP111 Jio model
FDL 
產測進版
 Add the command of the jio_mfg set hwVersion=R01 (R01A) in order to fix OQC fail issue
DCC=>1.
請問有驗證資料嗎
 
à
已驗證請參照如下
mail 
2.BAR 
單印度簽核確認
(6/29) 
à
 
這一次請參照附件的重工會議紀錄
 & 
開立的重工
K
工單
 
                                                                  
Hi Lung / Calvin  ,
請協助，長期對策
 
 : RI
系統有印度生產的需求，請協助系統更新
 
謝謝
!! 
 
From:
 may_wu 
吳美玉
 <

> 
Sent:
 Monday, June 29, 2026 5:16 PM
 wendy_chiu 
邱宇絃
 <

>
 alex_chiang 
江育誠
 <

>; wii_lin 
林偉能
 <

>; may_wu 
吳美玉
 <

>; ck_yang 
楊智凱
 <

>; rossi_chen 
陳旭
 <

>; calvin_chen 
陳漢鍾
 <

>; mareedu_rao Mareedu Chiranjeevi <

>; sebastian_huang 
黃胤誠
 <

>; lanqly_chou 
周偉堯
 <

>; spoo_wei 
魏墉伸
 <

>; simon_kang 
康信雄
 <

>; bill_chen 
陳奕廷
 <

>; austin_chang 
張金鐘
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>; kentchiou 
邱福壽
 <

>; alyssa_fan 
范秀景
 <

>; kelsey_tsai 
蔡易儒
 <

>; femehring_langhu Femehring Langhu <

>
Subject:
 FW: OQC phy ic version fail issue
 
+Wendy 
 
From:
 alex_chiang 
江育誠
 <

> 
Sent:
 Monday, June 29, 2026 4:54 PM
 wii_lin 
林偉能
 <

>; may_wu 
吳美玉
 <

>; ck_yang 
楊智凱
 <

>; rossi_chen 
陳旭
 <

>; calvin_chen 
陳漢鍾
 <

>
 mareedu_rao Mareedu Chiranjeevi <

>; sebastian_huang 
黃胤誠
 <

>; lanqly_chou 
周偉堯
 <

>; spoo_wei 
魏墉伸
 <

>; simon_kang 
康信雄
 <

>; bill_chen 
陳奕廷
 <

>; austin_chang 
張金鐘
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>; kentchiou 
邱福壽
 <

>; alyssa_fan 
范秀景
 <

>; kelsey_tsai 
蔡易儒
 <

>; femehring_langhu Femehring Langhu <

>
Subject:
 
回覆
: OQC phy ic version fail issue
 
Hi Wii
V5.0.5.5.1F.3.9 , V5.0.5.5.1F.1.0_RI , V5.0.5.5.1F.3.9
沒發現問題。
 
STATION ID: FDL
 Test Program Version: V5.0.5.5.1F.3.9
 
: 52 30 31 41 00 00 00 00 00 00 00 00 00 00 00 00  R01A............
 
12:08:49:608| root@OpenWrt:/# jio_mfg set hwVersion=R01A
12:08:54:655| set hwVersion to : 'R01A'
12:08:55:309| write MFG data to flash.
12:08:55:309| root@OpenWrt:/# jio_mfg get hwVersion
12:08:55:325| Hardware version: R01A
 
= 12:11:46:118| cas.pem                   | 10 kB |  10.6 kB/s | ETA: 00:00:00 | 100%                                                                         =
= 12:11:46:118| cert.pem                  | 1 kB |   1.8 kB/s | ETA: 00:00:00 | 100%                                                                          =
= 12:11:46:118| dev-id                    | 0 kB |   0.0 kB/s | ETA: 00:00:00 | 100%                                                                          =
= 12:11:46:118| key.pem                   | 1 kB |   1.6 kB/s | ETA: 00:00:00 | 100%                                                                          =
= 12:11:46:118| operational.ca            | 10 kB |  10.6 kB/s | ETA: 00:00:00 | 100%                                                                         =
= 12:11:46:118| operational.pem           | 1 kB |   1.8 kB/s | ETA: 00:00:00 | 100% 
 
DISTRIB_TIP='OpenWrt 23.05-SNAPSHOT r23485+90-e92cf0c46f / TIP-devel-01c94cf9'
 
 
STATION ID: OQC-F
Test Program Version: V5.0.5.5.1F.3.9
 
<time:12:22:36> Get HW info == R01A 
_f_CheckCertification
Check TIP version: DISTRIB_TIP='OpenWrt 23.05-SNAPSHOT r23485+90-e92cf0c46f / TIP-devel-01c94cf9' ;PASS
hexdump -C -s 0x6E -n 6 /dev/mtd7
0000006e  52 30 31 41 00 00                                 |R01A..|
 
3. STATION ID: FDL
Test Program Version: V5.0.5.5.1F.1.0_RI
 
-sb_fip.bin
: 52 30 31 41 00 00 00 00 00 00 00 00 00 00 00 00  R01A............
-sb_bl2.img
-openwrt-mediatek-mt7981-mt7981-spim-nand-rfb-sb-squashfs-sysupgrade.bin
jio_mfg init
jio_mfg set hwVersion=R01A
root@OpenWrt:/# jio_mfg get hwVersion
15:55:01:621| Hardware version: R01A
-eap111-5.0.5.5-jio-secureboot-fac-sysupgrade.bin
 
# 15:57:49:109| cas.pem                   | 10 kB |  10.6 kB/s | ETA: 00:00:00 | 100%                                                                                                                        #
# 15:57:49:109| cert.pem                  | 1 kB |   1.8 kB/s | ETA: 00:00:00 | 100%                                                                                                                         #
# 15:57:49:109| dev-id                    | 0 kB |   0.0 kB/s | ETA: 00:00:00 | 100%                                                                                                                         #
# 15:57:49:109| key.pem                   | 1 kB |   1.6 kB/s | ETA: 00:00:00 | 100%                                                                                                                         #
# 15:57:49:109| operational.ca            | 10 kB |  10.6 kB/s | ETA: 00:00:00 | 100%                                                                                                                        #
# 15:57:49:109| operational.pem           | 1 kB |   1.8 kB/s | ETA: 00:00:00 | 100%
 
Check TIP version: DISTRIB_TIP='OpenWrt 23.05-SNAPSHOT r23485+90-e92cf0c46f / TIP-devel-01c94cf9' ;PASS
寄件者
:
 wii_lin 
林偉能
 <

>
寄件日期
:
 2026
年
6
月
29
日
 
下午
 04:03
收件者
:
 may_wu 
吳美玉
 <

>; alex_chiang 
江育誠
 <

>; ck_yang 
楊智凱
 <

>; rossi_chen 
陳旭
 <

>; calvin_chen 
陳漢鍾
 <

>
:
 mareedu_rao Mareedu Chiranjeevi <

>; sebastian_huang 
黃胤誠
 <

>; lanqly_chou 
周偉堯
 <

>; spoo_wei 
魏墉伸
 <

>; simon_kang 
康信雄
 <

>; bill_chen 
陳奕廷
 <

>; wii_lin 
林偉能
 <

>; austin_chang 
張金鐘
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>; spoo_wei 
魏墉伸
 <

>; kentchiou 
邱福壽
 <

>; alyssa_fan 
范秀景
 <

>; kelsey_tsai 
蔡易儒
 <

>; femehring_langhu Femehring Langhu <

>
主旨
:
 
回覆
: OQC phy ic version fail issue
 
 
Hi May, Alex, CK, Rossi
 
RI / FDL / OQC FDL logfile
​
​
 
如附件
.
請確認
. 
謝謝
.
​
​
 
 
 
 
Best Wishes!
====================================
林偉能
 Wii_Lin
智邦科技
Accton Technology Corporation
新竹市科學工業園區
研
新三路一號
E-mail
：

 
寄件者
:
 may_wu 
吳美玉
 <

>
寄件日期
:
 2026
年
6
月
29
日
 
上午
 08:39
收件者
:
 calvin_chen 
陳漢鍾
 <

>
:
 may_wu 
吳美玉
 <

>; mareedu_rao Mareedu Chiranjeevi <

>; alex_chiang 
江育誠
 <

>; wii_lin 
林偉能
 <

>; ck_yang 
楊智凱
 <

>; sebastian_huang 
黃胤誠
 <

>; rossi_chen 
陳旭
 <

>; lanqly_chou 
周偉堯
 <

>; spoo_wei 
魏墉伸
 <

>; simon_kang 
康信雄
 <

>; bill_chen 
陳奕廷
 <

>; austin_chang 
張金鐘
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>; spoo_wei 
魏墉伸
 <

>; kentchiou 
邱福壽
 <

>; may_wu 
吳美玉
 <

>; alyssa_fan 
范秀景
 <

>; may_wu 
吳美玉
 <

>; kelsey_tsai 
蔡易儒
 <

>
主旨
:
 FW: OQC phy ic version fail issue
 
 
+Calvin 
 
From:
 may_wu 
吳美玉
 
Sent:
 Thursday, June 25, 2026 7:58 PM
 mareedu_rao Mareedu Chiranjeevi <

>; alex_chiang 
江育誠
 <

>; wii_lin 
林偉能
 <

>; ck_yang 
楊智凱
 <

>; sebastian_huang 
黃胤誠
 <

>; rossi_chen 
陳旭
 <

>; lanqly_chou 
周偉堯
 <

>; spoo_wei 
魏墉伸
 <

>
 simon_kang 
康信雄
 <

>; bill_chen 
陳奕廷
 <

>; austin_chang 
張金鐘
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>; spoo_wei 
魏墉伸
 <

>; kentchiou 
邱福壽
 <

>; may_wu 
吳美玉
 <

>; alyssa_fan 
范秀景
 <

>
Subject:
 RE: OQC phy ic version fail issue
 
Hi All ,
Meeting minute ,
ATT : Wii / Mareedu_rao  / CK / Alex / Calvin / May 
 
1. ECN / SWR Implementation ,Owner: All , Due :6/26 
 
2. Test Program Upgrade
     1.  A  from V5.0.5.5.1F.3.8 to V5.0.5.5.1F.3.9
           Reason : Add command:jio_mfg set hwVersion=R01(for R01A units) to resolve the OQC failure issue.
     2.  Pre-production test log have been provided and confirmed by Wii and Alex 
     3. Update OQC test program and provide pre-production test log for verification, Owner: Rossi / Wii  ,Due:6/26
 
3. G266004N : 50pcs WIP rework 
     - It has been confirmed that there are 50 units produced using the previous test program version (V5.0.5.5.1F.3.8) that require rework.
   - Provide the serial number list for the 50 units. Owner: Wii ,Due :6/ 26
     - Provide the rework test program and link . Owner: CK ,Due: 6/26 
         - >Pre-production testing using the new OQC test program and provide test log for verification. Owner: Wii / Alex ,Due : 6 / 26
     - Provide K Work Order and Work Order Checklist. Owner: Spoo / Calvin , Due:6/ 26
     - Rework Instructions
       CI2WLP111005E *50 pcs
        Compare old and new serial number records; S/N and MAC ID must remain unchanged.
        Perform retesting using the rework test program.
         OQC testing for all reworked units.
 
 Thank you.
 
From:
 mareedu_rao Mareedu Chiranjeevi <

> 
Sent:
 Thursday, June 25, 2026 3:05 PM
 alex_chiang 
江育誠
 <

>; wii_lin 
林偉能
 <

>; ck_yang 
楊智凱
 <

>; sebastian_huang 
黃胤誠
 <

>; rossi_chen 
陳旭
 <

>; lanqly_chou 
周偉堯
 <

>; may_wu 
吳美玉
 <

>
 simon_kang 
康信雄
 <

>; bill_chen 
陳奕廷
 <

>; austin_chang 
張金鐘
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>
Subject:
 Re: OQC phy ic version fail issue
 
Hi 
@ck_yang 
楊智凱
 & 
@may_wu 
吳美玉
,
 
Right now, Jio PDI OQC stage not performing OQC tests with New PHY IC devices. All new PHY devices are on hold at PK-1 Stage  (Jio PDI team waiting for ECN).
 
Once, ECN complete, we can start using FDL TP & OQC NEW PHY TP. When can we expect the ECN complete date?
 
Tks
Chiranjeevi
From:
 alex_chiang 
江育誠
 <

>
Sent:
 24 June 2026 18:39
 mareedu_rao Mareedu Chiranjeevi <

>; wii_lin 
林偉能
 <

>; ck_yang 
楊智凱
 <

>; sebastian_huang 
黃胤誠
 <

>; rossi_chen 
陳旭
 <

>; lanqly_chou 
周偉堯
 <

>
 may_wu 
吳美玉
 <

>; simon_kang 
康信雄
 <

>; bill_chen 
陳奕廷
 <

>; austin_chang 
張金鐘
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>
Subject:
 
回覆
: OQC phy ic version fail issue
 
 
Hi Will , Rossi , CK,
 
FDL : No problems found,
OQC: 
@rossi_chen 
陳旭
 
What criteria does your R01A use to determine
whether the current DUT is R01 or R01A?
 
Product: EAP111-0223-WL
 
FDL:
Test Program Version: V5.0.5.5.1F.3.: 52 30 31 41 00 00 00 00 00 00 00 00 00 00 00 00  R01A............
15:29:05:720| set hwVersion to : 'R01'
15:29:06:676| root@OpenWrt:/# jio_mfg set hwVersion=R01A
15:29:12:374| root@OpenWrt:/# jio_mfg get hwVersion
15:29:12:390| Hardware version: R01A
MT7981> setenv model_revision R01A
 
OQC:
STATION ID: OQC-F
Test Program Version: V5.0.5.5.1F.3.7
hexdump -C -s 0x6E -n 6 /dev/mtd7
0000006e  52 30 31 41 00 00                                 |R01A..|
 <time:15:39:55> Check Hardware ver = R01A ;PASS    
寄件者
:
 mareedu_rao Mareedu Chiranjeevi <

>
寄件日期
:
 2026
年
6
月
24
日
 
下午
 06:42
收件者
:
 wii_lin 
林偉能
 <

>; ck_yang 
楊智凱
 <

>; sebastian_huang 
黃胤誠
 <

>; rossi_chen 
陳旭
 <

>; alex_chiang 
江育誠
 <

>; lanqly_chou 
周偉堯
 <

>
:
 may_wu 
吳美玉
 <

>; simon_kang 
康信雄
 <

>; bill_chen 
陳奕廷
 <

>; austin_chang 
張金鐘
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>
主旨
:
 Re: OQC phy ic version fail issue
 
 
Hi 
@ck_yang 
楊智凱
 
@wii_lin 
林偉能
 
FDL tested with new TP V3.9 (REGAPFM)
 
TEST - PASS 
 
Same device, OQC Test PASS with new_phy TP.
 
Test log files attached.
 
Tks
Chiranjeevi
From:
 wii_lin 
林偉能
 <

>
Sent:
 24 June 2026 12:47
 mareedu_rao Mareedu Chiranjeevi <

>; ck_yang 
楊智凱
 <

>; sebastian_huang 
黃胤誠
 <

>; rossi_chen 
陳旭
 <

>; alex_chiang 
江育誠
 <

>; lanqly_chou 
周偉堯
 <

>
 wii_lin 
林偉能
 <

>; may_wu 
吳美玉
 <

>; simon_kang 
康信雄
 <

>; bill_chen 
陳奕廷
 <

>; austin_chang 
張金鐘
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>
Subject:
 
回覆
: OQC phy ic version fail issue
 
 
Hi 
Chiranjeevi 
 
Download the Production Test V3.9 to verify the FDL TP, then use the OQC New PHY TP for verification, and attach the verification log file.
 
Report by 3:00 PM.
 
 
 
Best Wishes!
====================================
林偉能
 Wii_Lin
智邦科技
Accton Technology Corporation
新竹市科學工業園區
研
新三路一號
E-mail
：

 
 
 
寄件者
:
 ck_yang 
楊智凱
 <

>
已傳送
:
 
星期三
, 2026 
年
 6 
月
 24 
日
 
下午
 12:05
收件者
:
 wii_lin 
林偉能
 <

>; sebastian_huang 
黃胤誠
 <

>; mareedu_rao Mareedu Chiranjeevi <

>; rossi_chen 
陳旭
 <

>; alex_chiang 
江育誠
 <

>; lanqly_chou 
周偉堯
 <

>
:
 may_wu 
吳美玉
 <

>; simon_kang 
康信雄
 <

>; bill_chen 
陳奕廷
 <

>; austin_chang 
張金鐘
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>
主旨
:
 
回覆
: OQC phy ic version fail issue 
 
Hi Wii:
           
以下為修改後產測
V3.9 
版本連結
:
                        
​
​
EAP111-0223-WL_V5.0.5.5.1F.3.9_FDL.7z
​
​
           MT151 
已經開啟
,
請下載驗證後
PASS LOG 
請寄出麻煩
Alex 
確認
 
 
Hi May:
           
由於產測有修改
,
需要切
ECN~~
 
 
 
Best Regards
CK
寄件者
:
 wii_lin 
林偉能
 <

>
寄件日期
:
 2026
年
6
月
24
日
 
下午
 02:00
收件者
:
 sebastian_huang 
黃胤誠
 <

>; ck_yang 
楊智凱
 <

>; mareedu_rao Mareedu Chiranjeevi <

>; rossi_chen 
陳旭
 <

>; alex_chiang 
江育誠
 <

>; lanqly_chou 
周偉堯
 <

>
:
 may_wu 
吳美玉
 <

>; simon_kang 
康信雄
 <

>; bill_chen 
陳奕廷
 <

>; austin_chang 
張金鐘
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>; wii_lin 
林偉能
 <

>
主旨
:
 Re: OQC phy ic version fail issue
 
Hi CK
 
請問什麼時候提供
TP
呢？
 
 
取得
 
iOS 
版
 Outlook
寄件者
:
 sebastian_huang 
黃胤誠
 <

>
寄件日期
:
 Wednesday, 24 June 2026 11:25:37
收件者
:
 ck_yang 
楊智凱
 <

>; mareedu_rao Mareedu Chiranjeevi <

>; rossi_chen 
陳旭
 <

>; wii_lin 
林偉能
 <

>; alex_chiang 
江育誠
 <

>; lanqly_chou 
周偉堯
 <

>
:
 may_wu 
吳美玉
 <

>; simon_kang 
康信雄
 <

>; bill_chen 
陳奕廷
 <

>; austin_chang 
張金鐘
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>
主旨
:
 
回覆
: OQC phy ic version fail issue
 
Hi CK,
 
The latest FDL log looks good to me.
 
 
Best Regards,
Sebastian
 
 
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
6
月
24
日
 11:50
收件者
:
 mareedu_rao Mareedu Chiranjeevi <

>; rossi_chen 
陳旭
 <

>; wii_lin 
林偉能
 <

>; alex_chiang 
江育誠
 <

>; lanqly_chou 
周偉堯
 <

>
:
 may_wu 
吳美玉
 <

>; simon_kang 
康信雄
 <

>; bill_chen 
陳奕廷
 <

>; austin_chang 
張金鐘
 <

>; sebastian_huang 
黃胤誠
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>
主旨
:
 
回覆
: OQC phy ic version fail issue
 
Hi Sebastian:
               Please help check the new FDL test log to investigate the Jio MFG hardware version issue.
 
 
 
Best Regards
CK
寄件者
:
 mareedu_rao Mareedu Chiranjeevi <

>
寄件日期
:
 2026
年
6
月
23
日
 
下午
 07:13
收件者
:
 rossi_chen 
陳旭
 <

>; wii_lin 
林偉能
 <

>; alex_chiang 
江育誠
 <

>; ck_yang 
楊智凱
 <

>; lanqly_chou 
周偉堯
 <

>
:
 may_wu 
吳美玉
 <

>; simon_kang 
康信雄
 <

>; bill_chen 
陳奕廷
 <

>; austin_chang 
張金鐘
 <

>; sebastian_huang 
黃胤誠
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>
主旨
:
 Re: OQC phy ic version fail issue
 
Hi 
@rossi_chen 
陳旭
 & 
@wii_lin 
林偉能
 
 
Please find the below update with latest OQC TP
 
 
Old PHY device - REGAPFM
OQC TP : CM_EAP111-0223-WL_V5.0.5.5_OQC_2026_05_21_002_old_phy
Test status - 
PASS 
(Log file attached)
 
 
 
New PHY device - REGAPFM 
OQC TP : CM_EAP111-0223-WL_V5.0.5.5_OQC_2026_06_23_001_new_phy
Test status - 
FAIL 
(Log file attached)
 
 
 
Please check.
 
Tks
Chiranjeevi
 
 
 
From:
 rossi_chen 
陳旭
 <

>
Sent:
 23 June 2026 14:18
 wii_lin 
林偉能
 <

>; alex_chiang 
江育誠
 <

>; ck_yang 
楊智凱
 <

>; lanqly_chou 
周偉堯
 <

>
 may_wu 
吳美玉
 <

>; simon_kang 
康信雄
 <

>; bill_chen 
陳奕廷
 <

>; austin_chang 
張金鐘
 <

>; sebastian_huang 
黃胤誠
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; mareedu_rao Mareedu Chiranjeevi <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>
Subject:
 RE: OQC phy ic version fail issue
 
Hi, Wii
因
FDL
程式修正，重新修改
OQC
程式
程式已放入網路磁碟內
謝謝
 
 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Engineer / Rossi_chen  
陳旭
電話
 :  #3019
Mail :
智
 
邦
 
科
 
技
 
股
 
份
 
有
 
份
 
公
 
司
Accton Technology Corporation
302
新竹縣竹北市智慧一路
1
號
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
From:
 alex_chiang 
江育誠
 <

>
Sent:
 Tuesday, June 23, 2026 4:07 PM
 ck_yang 
楊智凱
 <

>; wii_lin 
林偉能
 <

>; lanqly_chou 
周偉堯
 <

>; rossi_chen 
陳旭
 <

>
 may_wu 
吳美玉
 <

>; simon_kang 
康信雄
 <

>; bill_chen 
陳奕廷
 <

>; austin_chang 
張金鐘
 <

>; sebastian_huang 
黃胤誠
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; mareedu_rao Mareedu Chiranjeevi <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>
Subject:
 
回覆
: OQC phy ic version fail issue
 
Hi Wii,
OQC REGAPFM_PASS_Y_1_124246.txt logfile
 
Product: EAP111-0223-WL
STATION ID: OQC-F
* SN: REGAPFM                                *
* MAC: 4445BA2B33D8                                  *
Test Program Version: V5.0.5.5.1F.3.7
Test Date and Start Time: 2026/06/23 12:42:46
 
已知問題
:
hexdump -C -s 0x6E -n 6 /dev/mtd7
0000006e  52 30 31 00 00 00                                 |R01...|
# <time:12:45:08> Check Hardware ver = R01 ;PASS     #
 
CK
新的產測會修正此
bug,
所以
OQC
如果是新的產測
FDL
後
 hexdump -C -s 0x6E -n 6 /dev/mtd7 
會得到
R01A
，提議
hexdump -C -s 0x6E -n 6 /dev/mtd7 
跟
 fw_printenv  model_revision 
比對，
相同
 ->  pass ,
不相同
 -> fail.
 
:~# fw_printenv  model_revision
model_revision=R01A
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
6
月
23
日
 
下午
 03:47
收件者
:
 wii_lin 
林偉能
 <

>; lanqly_chou 
周偉堯
 <

>; rossi_chen 
陳旭
 <

>
:
 may_wu 
吳美玉
 <

>; alex_chiang 
江育誠
 <

>; simon_kang 
康信雄
 <

>; bill_chen 
陳奕廷
 <

>; austin_chang 
張金鐘
 <

>; sebastian_huang 
黃胤誠
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; mareedu_rao Mareedu Chiranjeevi <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>
主旨
:
 
回覆
: OQC phy ic version fail issue
 
Hi Sebastian:
                     
如附檔
,
已經修改
,
請再確認
FDL test log 
                     PS: 
驗證機台為
R01 
版本
 
                     
             
  
Best Regards
CK
 
寄件者
:
 wii_lin 
林偉能
 <

>
寄件日期
:
 2026
年
6
月
23
日
 
下午
 03:25
收件者
:
 lanqly_chou 
周偉堯
 <

>; ck_yang 
楊智凱
 <

>; rossi_chen 
陳旭
 <

>
:
 wii_lin 
林偉能
 <

>; may_wu 
吳美玉
 <

>; alex_chiang 
江育誠
 <

>; simon_kang 
康信雄
 <

>; bill_chen 
陳奕廷
 <

>; austin_chang 
張金鐘
 <

>; sebastian_huang 
黃胤誠
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; mareedu_rao Mareedu Chiranjeevi <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>
主旨
:
 
回覆
: OQC phy ic version fail issue
 
Hi Rossi, Lanqly, CK
 
新
 PHY OQC TP test logfile 
如附件
. 
請確認
.
​​
另外
, 
下列狀態什麼時候可以提供給 產線 驗證呢
?
--> 
請再提供
TRD 
指令針對
FDL 
站
PHY IC 
版本
(R01,R01A) 
讓產測最後寫入覆蓋之前寫的
,
 
 
Best Wishes!
====================================
林偉能
 Wii_Lin
智邦科技
Accton Technology Corporation
新竹市科學工業園區
研
新三路一號
E-mail
：

 
寄件者
:
 wii_lin 
林偉能
 <

>
寄件日期
:
 2026
年
6
月
22
日
 
下午
 05:31
收件者
:
 lanqly_chou 
周偉堯
 <

>; ck_yang 
楊智凱
 <

>; rossi_chen 
陳旭
 <

>
:
 may_wu 
吳美玉
 <

>; alex_chiang 
江育誠
 <

>; simon_kang 
康信雄
 <

>; bill_chen 
陳奕廷
 <

>; wii_lin 
林偉能
 <

>; austin_chang 
張金鐘
 <

>; sebastian_huang 
黃胤誠
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; mareedu_rao Mareedu Chiranjeevi <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>
主旨
:
 
回覆
: OQC phy ic version fail issue
 
Hi Rossi, Lanqly, CK
 
舊
 PHY OQC TP test logfile 
如附件
. 
請確認
.
​​
另外
, 
下列狀態什麼時候可以提供給 產線 驗證呢
?
--> 
請再提供
TRD 
指令針對
FDL 
站
PHY IC 
版本
(R01,R01A) 
讓產測最後寫入覆蓋之前寫的
,
 
 
Best Wishes!
====================================
林偉能
 Wii_Lin
智邦科技
Accton Technology Corporation
新竹市科學工業園區
研
新三路一號
E-mail
：

 
 
 
寄件者
:
 lanqly_chou 
周偉堯
 <

>
已傳送
:
 
星期一
, 2026 
年
 6 
月
 22 
日
 
下午
 03:34
收件者
:
 ck_yang 
楊智凱
 <

>; wii_lin 
林偉能
 <

>; rossi_chen 
陳旭
 <

>
:
 may_wu 
吳美玉
 <

>; alex_chiang 
江育誠
 <

>; simon_kang 
康信雄
 <

>; bill_chen 
陳奕廷
 <

>; austin_chang 
張金鐘
 <

>; sebastian_huang 
黃胤誠
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; mareedu_rao Mareedu Chiranjeevi <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>
主旨
:
 
回覆
: OQC phy ic version fail issue
 
Dear Bill and Sebastian,
 
Please help on this, modify TRD to support this scenario.
 
Best regards,
Lanqly
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
6
月
22
日
 17:41
收件者
:
 wii_lin 
林偉能
 <

>; rossi_chen 
陳旭
 <

>; lanqly_chou 
周偉堯
 <

>
:
 may_wu 
吳美玉
 <

>; alex_chiang 
江育誠
 <

>; simon_kang 
康信雄
 <

>; austin_chang 
張金鐘
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; mareedu_rao Mareedu Chiranjeevi <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>
主旨
:
 
回覆
: OQC phy ic version fail issue
 
Hi Lanqly:
           
請再提供
TRD 
指令針對
FDL 
站
PHY IC 
版本
(R01,R01A) 
讓產測最後寫入覆蓋之前寫的
,
           
另外請注意這指令不要影響到其他已經寫入資料
(ex: uboot password)
        
 
Best Regards
CK
寄件者
:
 wii_lin 
林偉能
 <

>
寄件日期
:
 2026
年
6
月
22
日
 
下午
 05:07
收件者
:
 rossi_chen 
陳旭
 <

>; lanqly_chou 
周偉堯
 <

>; ck_yang 
楊智凱
 <

>
:
 may_wu 
吳美玉
 <

>; alex_chiang 
江育誠
 <

>; simon_kang 
康信雄
 <

>; austin_chang 
張金鐘
 <

>; wii_lin 
林偉能
 <

>; victor_wang 
王紹誠
 <

>; Ashok Pal <

>; Shivangi Sujal <

>; Kajal Thakur <

>; ravi_kant Ravi Kant <

>; mareedu_rao Mareedu Chiranjeevi <

>; peifang_hung 
洪珮芳
 <

>; enco 
劉升順
 <

>; may_wu 
吳美玉
 <

>
主旨
:
 
回覆
: OQC phy ic version fail issue
 
Hi Rossi
 
請優化
 OQC TP R01 --> R01A (
注意 舊
 PHY 
與 新
 PHY 
問題
).
 
 
 
Hi Lanqly
 
Jio_mfg init 
仍寫
R01 --> 
請反饋給 客戶 解決該問題
. 
(JIO PDI team 
已將生產工站
 PK-1 & PK-2 hold 
住
)
 
 
Best Wishes!
====================================
林偉能
 Wii_Lin
智邦科技
Accton Technology Corporation
新竹市科學工業園區
研
新三路一號
E-mail
：

 
 
 
寄件者
:
 lanqly_chou 
周偉堯
 <

>
已傳送
:
 
星期一
, 2026 
年
 6 
月
 22 
日
 
下午
 02:27
收件者
:
 ck_yang 
楊智凱
 <

>
:
 may_wu 
吳美玉
 <

>; alex_chiang 
江育誠
 <

>; rossi_chen 
陳旭
 <

>; wii_lin 
林偉能
 <

>; simon_kang 
康信雄
 <

>
主旨
:
 
回覆
: OQC phy ic version fail issue
 
Hi CK,
 
沒錯
, 
高機率是這個問題
. 
看起來
 Jio 
的
 jio_mfg 
覆寫了
 HW revision. 
我們有機會在跑完
 jio_mfg 
後再覆蓋一次嗎
?
 
Best regards,
Lanqly
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
6
月
22
日
 16:52
收件者
:
 lanqly_chou 
周偉堯
 <

>
:
 may_wu 
吳美玉
 <

>; alex_chiang 
江育誠
 <

>; rossi_chen 
陳旭
 <

>; wii_lin 
林偉能
 <

>; simon_kang 
康信雄
 <

>
主旨
:
 OQC phy ic version fail issue
 
Hi Lanqly:
           
 
剛剛
Wii 
反應在印度產線遇到一個問題
:
 
一台機器在
FDL 
讀出最後確認寫入
R01A 
版本
(
如圖一
) 
 
但在
FDL 
之後
OQC 
檢測站讀出
FAIL ,
因為讀出卻是
R01
(
如圖二
)
 
跟你確認產測過程中有
Jio_mfg init  script 
這段
code 
還是寫入
R01
 
是否這樣以致
OQC 
讀到也是
R01(
如圖三
),
而不是
R01A
 
麻煩請確認
,
謝謝
 
 
<
產測最後寫入
R01A, 
圖一
>
 
 
<QOC 
測試站檢測讀出
R01,
圖二
>
 
 
 
 
圖三
 Jio_mfg init 
仍寫
R01:
 
Best Regards
CK
