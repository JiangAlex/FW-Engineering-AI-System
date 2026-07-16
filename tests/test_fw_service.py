import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.fw_service import FWService


class TestExtractInfoByLine:
    """Tests for context-aware model-version extraction."""

    def test_embedded_string_extraction(self):
        """Model embedded in filename string extracts model+version directly."""
        text = "EAP111-0223-WL_V5.0.5.5.1F.3.7_FDL"
        result = FWService.extract_info_by_line(text)
        assert "EAP111" in result
        assert "5.0.5.5.1F.3.7" in result["EAP111"]

    def test_four_segment_version(self):
        """4-segment version with FW prefix pairs globally."""
        text = "ECS4100 TIP Upgrade\nFW V2.2.14.261"
        result = FWService.extract_info_by_line(text)
        assert "ECS4100" in result
        assert "2.2.14.261" in result["ECS4100"]

    def test_proximity_within_10_lines(self):
        """Version within ±10 lines of model pairs."""
        lines = ["EAP115 production"] + ["other content"] * 5 + ["version 2.3.1.0"]
        text = "\n".join(lines)
        result = FWService.extract_info_by_line(text)
        assert "EAP115" in result
        assert "2.3.1.0" in result["EAP115"]

    def test_high_confidence_global_pairing(self):
        """Version with V prefix pairs with all models regardless of distance."""
        lines = ["EAP115 device"] + ["filler"] * 50 + ["FW V4.2.0"]
        text = "\n".join(lines)
        result = FWService.extract_info_by_line(text)
        assert "EAP115" in result
        assert "4.2.0" in result["EAP115"]

    def test_no_match_bare_number_far_away(self):
        """Bare number like 0.5 far from model should NOT pair."""
        lines = ["EAP111 device info"] + ["filler"] * 80 + ["estimated 0.5 day"]
        text = "\n".join(lines)
        result = FWService.extract_info_by_line(text)
        if "EAP111" in result:
            assert "0.5" not in result["EAP111"]

    def test_multi_model_isolation(self):
        """Each model only gets its nearby low-confidence versions."""
        lines = (
            ["EAP115 info", "version 4.2.0.1"]
            + ["filler"] * 30
            + ["ECS4100 info", "version 2.2.14.261"]
        )
        text = "\n".join(lines)
        result = FWService.extract_info_by_line(text)
        assert "EAP115" in result
        assert "ECS4100" in result
        assert "2.2.14.261" not in result.get("EAP115", set())
        assert "4.2.0.1" not in result.get("ECS4100", set())

    def test_jws_model_recognized(self):
        """JWS model series is recognized."""
        text = "JWS2261P firmware\nV4.1.2"
        result = FWService.extract_info_by_line(text)
        assert "JWS2261P" in result
        assert "4.1.2" in result["JWS2261P"]

    def test_alias_normalization_eap115a(self):
        """EAP115a normalizes to EAP115."""
        text = "EAP115a device\nFW V4.2.0"
        result = FWService.extract_info_by_line(text)
        assert "EAP115" in result
        assert "EAP115A" not in result

    def test_alias_normalization_jiowave(self):
        """JioWave62420 normalizes to EAP111."""
        text = "JioWave62420 production\nFW V5.0.5.5"
        result = FWService.extract_info_by_line(text)
        assert "EAP111" in result
        assert "JIOWAVE62420" not in result
