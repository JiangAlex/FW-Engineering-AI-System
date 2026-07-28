import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.core.parser import extract_chunks
from src.core.database import init_chunks_db, clear_chunks, insert_chunk, search_chunks, get_all_models, DB_PATH
import sqlite3

SAMPLE_MD = """# EAP111 Test Email

- Sender: test@test.com
- Date: Wed, 1 Apr 2026 07:49:02 +0000
- Source File: test.msg

---

## ✅ Summary
PKI 2.0 upgrade needed

---

## ✅ Clean Content
Hi all,
今日會議記錄如下
重工原因: PKI2.0 進版
重工數量: 50
Model: EAP111
FW Version: V5.0.5.5
測試結果 PASS
產測程式版本 V1.1
This is line 8
This is line 9
This is line 10
This is line 11
This is line 12
This is line 13
This is line 14
This is line 15
This is line 16
This is line 17
This is line 18
This is line 19
This is line 20
This is line 21
This is line 22 second chunk

---

## ✅ Full Content
This should NOT be indexed
"""

SAMPLE_MD_EAP115 = """# EAP115 NAND ECN

- Sender: test@test.com
- Date: Fri, 15 May 2026 03:00:00 +0000
- Source File: eap115.msg

---

## ✅ Summary
NAND flash change

---

## ✅ Clean Content
EAP115 NAND ECN add MX35LF1GE4ABZ4IG
Flash migration from W25N01GV to W25N01KV
需要 AP-code 更新

---

## ✅ Full Content
repeated content
"""


class TestExtractChunks:
    def test_extracts_clean_content_only(self):
        result = extract_chunks(SAMPLE_MD, "EAP111 test.md")
        all_text = " ".join(result["chunks"])
        assert "PKI2.0" in all_text
        assert "should NOT be indexed" not in all_text

    def test_splits_into_chunks(self):
        result = extract_chunks(SAMPLE_MD, "EAP111 test.md")
        assert len(result["chunks"]) >= 2  # >20 non-empty lines → 2 chunks

    def test_extracts_model(self):
        result = extract_chunks(SAMPLE_MD, "EAP111 test.md")
        assert "EAP111" in result["model"]

    def test_extracts_date(self):
        result = extract_chunks(SAMPLE_MD, "EAP111 test.md")
        assert result["date_str"] == "2026-04-01"

    def test_model_normalization(self):
        md = SAMPLE_MD.replace("EAP111", "JioWave62420")
        result = extract_chunks(md, "JioWave62420 test.md")
        assert "EAP111" in result["model"]

    def test_fallback_to_full_content_when_clean_too_short(self):
        """When Clean Content < 100 chars, should fallback to Full Content."""
        md = """# Test Short Clean

- Sender: test@test.com
- Date: Thu, 7 May 2026 11:33:46 +0000
- Source File: test.msg

---

## ✅ Summary
Review OK.

---

## ✅ Clean Content
Hi CK,
Review OK. Thanks.
Best regards,
Lanqly

---

## ✅ Full Content
Hi CK,
Review OK. Thanks.
Best regards,
Lanqly
From: alex_chiang
Date: 2026-05-07
Subject: OEL Production readiness
Hi Lanqly,
Please review and double check the FDL test log for FW V5.0.5.5.
The latest test program has been uploaded to the OEL FTP site.
EAP111 production firmware ready.
Best Regards,
CK
"""
        result = extract_chunks(md, "JioWave62420 OEL Production readiness.md")
        all_text = " ".join(result["chunks"])
        # Should contain content from the reply chain (Full Content)
        assert "FW V5.0.5.5" in all_text or "FDL test log" in all_text
        assert "EAP111" in result["model"]

    def test_no_fallback_when_clean_is_long_enough(self):
        """When Clean Content >= 100 chars, should NOT fallback to Full Content."""
        result = extract_chunks(SAMPLE_MD, "EAP111 test.md")
        all_text = " ".join(result["chunks"])
        assert "should NOT be indexed" not in all_text

    def test_empty_clean_falls_back_to_full(self):
        """When Clean Content is empty, fallback to Full Content."""
        md = "# Empty\n- Date: \n---\n## ✅ Clean Content\n\n---\n## ✅ Full Content\nstuff"
        result = extract_chunks(md, "empty.md")
        assert result["chunks"] == ["stuff"]

    def test_truly_empty_content(self):
        """When both Clean and Full Content are empty, no chunks."""
        md = "# Empty\n- Date: \n---\n## ✅ Clean Content\n\n---\n## ✅ Full Content\n"
        result = extract_chunks(md, "empty.md")
        assert result["chunks"] == []


@pytest.fixture
def chunks_db(tmp_path, monkeypatch):
    """Use a temporary DB for testing."""
    db_path = str(tmp_path / "test.db")
    monkeypatch.setattr("src.core.database.DB_PATH", db_path)
    init_chunks_db()
    return db_path


class TestSearchChunks:
    def test_basic_search(self, chunks_db):
        insert_chunk("test.md", "PKI 2.0 重工原因 EAP111", "EAP111", "2026-04-01")
        results = search_chunks("PKI")
        assert len(results) >= 1
        assert "PKI" in results[0]["chunk_text"]

    def test_bm25_ranking(self, chunks_db):
        insert_chunk("a.md", "unrelated content about nothing", "EAP115", "2026-01-01")
        insert_chunk("b.md", "PKI PKI PKI 2.0 upgrade PKI certificate", "EAP111", "2026-04-01")
        insert_chunk("c.md", "PKI mentioned once", "EAP111", "2026-03-01")
        results = search_chunks("PKI")
        # b.md should rank higher (more PKI mentions)
        assert results[0]["filename"] == "b.md"

    def test_model_filter(self, chunks_db):
        insert_chunk("a.md", "PKI upgrade for EAP111", "EAP111", "2026-04-01")
        insert_chunk("b.md", "PKI upgrade for EAP115", "EAP115", "2026-04-01")
        results = search_chunks("PKI", model="EAP115")
        assert all("EAP115" in r["model"] for r in results)

    def test_date_filter(self, chunks_db):
        insert_chunk("old.md", "PKI old info", "EAP111", "2025-01-01")
        insert_chunk("new.md", "PKI new info", "EAP111", "2026-05-01")
        results = search_chunks("PKI", date_from="2026-01-01")
        assert all(r["date_str"] >= "2026-01-01" for r in results)

    def test_no_results(self, chunks_db):
        insert_chunk("a.md", "hello world", "EAP111", "2026-04-01")
        results = search_chunks("ZZZZNONEXISTENT")
        assert results == []

    def test_get_all_models(self, chunks_db):
        insert_chunk("a.md", "text", "EAP111,EAP115", "2026-04-01")
        insert_chunk("b.md", "text", "JWS2261P", "2026-04-01")
        models = get_all_models()
        assert "EAP111" in models
        assert "EAP115" in models
        assert "JWS2261P" in models
