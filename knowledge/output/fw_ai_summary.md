## ✅ Key Points
- **EAP115**: Firmware V4.2.0 (pki2.0) for TIP; second‑source FLASH (MXIC 4‑bit ECC) needs AP‑code update.  
- **EAP104 TE/TEL**: Share identical TIP FDL (V4.1.1, checksum C606) but differ only in certificate (Edgecore PKI 2.0).  
- **SC48P / ECS4100**: Unified SW upgrade to V2.2.14.261 with matching production‑test program (V2.2.14.261_0Y1.31); tied to ECN260400022.  
- **JWS2261P / JWS4261P**: OLS 4.1.2 with PKI 2.0 for Jio.  
- **EAP111 (Jio)**: Secure‑boot uboot updated (20260514‑sb_fip.bin) for PKI 2.0.

## ✅ Analysis
The EAP series maintains stable firmware bases while handling certificate variants by swapping only the certificate type, keeping version numbers consistent (e.g., EAP104 V4.1.1, EAP115 V4.2.0). The SC48P/ECS4100 share the same V2.2.14.261, indicating coordinated cross‑product upgrades via a single ECN. The second‑source FLASH migration for EAP115 is the main risk point, requiring AP‑code synchronization to prevent divergence.

## ✅ Conclusion
Firmware versioning across EAP/ECS lines is internally consistent, but the EAP115 second‑source FLASH migration and the synchronized SC48P/ECS4100 upgrade must be closely monitored to avoid version drift.