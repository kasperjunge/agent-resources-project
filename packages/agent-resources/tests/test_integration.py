"""Integration tests that simulate real-world usage."""

import sys
import tempfile
import tarfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path for non-installed testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agent_resources.fetcher import fetch_resource, ResourceType
from agent_resources.exceptions import ResourceNotFoundError
import httpx


def create_mock_repo_tarball(tmp_path: Path, repo_name: str, structure: str) -> bytes:
    """Create a mock GitHub tarball with specified structure.
    
    Args:
        tmp_path: Temporary directory path
        repo_name: Name of the repository
        structure: Type of structure - 'claude', 'anthropics', or 'opencode'
    
    Returns:
        Tarball bytes
    """
    # Create repo directory structure
    repo_dir = tmp_path / f"{repo_name}-main"
    
    if structure == "claude":
        # .claude/skills/test-skill/ structure
        skill_dir = repo_dir / ".claude" / "skills" / "test-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("# Test Skill (Claude structure)")
        
        cmd_dir = repo_dir / ".claude" / "commands"
        cmd_dir.mkdir(parents=True)
        (cmd_dir / "test-cmd.md").write_text("# Test Command (Claude structure)")
        
    elif structure == "anthropics":
        # skills/test-skill/ structure
        skill_dir = repo_dir / "skills" / "test-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("# Test Skill (Anthropics structure)")
        
        cmd_dir = repo_dir / "commands"
        cmd_dir.mkdir(parents=True)
        (cmd_dir / "test-cmd.md").write_text("# Test Command (Anthropics structure)")
        
    elif structure == "opencode":
        # skill/test-skill/ structure
        skill_dir = repo_dir / "skill" / "test-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("# Test Skill (OpenCode structure)")
        
        cmd_dir = repo_dir / "command"
        cmd_dir.mkdir(parents=True)
        (cmd_dir / "test-cmd.md").write_text("# Test Command (OpenCode structure)")
    
    # Create tarball
    tarball_path = tmp_path / "repo.tar.gz"
    with tarfile.open(tarball_path, "w:gz") as tar:
        tar.add(repo_dir, arcname=f"{repo_name}-main")
    
    return tarball_path.read_bytes()


def test_backward_compatibility_claude_structure():
    """Test backward compatibility with .claude/skills structure"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        dest_path = tmp_path / "destination"
        
        # Create mock tarball with Claude structure
        tarball_bytes = create_mock_repo_tarball(tmp_path / "source", "agent-resources", "claude")
        
        # Mock httpx response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = tarball_bytes
        
        with patch('httpx.Client') as mock_client:
            mock_client.return_value.__enter__.return_value.get.return_value = mock_response
            
            # Should work with default repo name
            result = fetch_resource(
                "testuser",
                "test-skill",
                dest_path,
                ResourceType.SKILL,
                overwrite=False,
                repo="agent-resources"
            )
            
            assert result.exists()
            assert result.name == "test-skill"
            assert (result / "SKILL.md").exists()
            content = (result / "SKILL.md").read_text()
            assert "Claude structure" in content


def test_anthropics_pattern_detection():
    """Test pattern detection for Anthropics-style repos (skills/)"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        dest_path = tmp_path / "destination"
        
        # Create mock tarball with Anthropics structure
        tarball_bytes = create_mock_repo_tarball(tmp_path / "source", "skills", "anthropics")
        
        # Mock httpx response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = tarball_bytes
        
        with patch('httpx.Client') as mock_client:
            mock_client.return_value.__enter__.return_value.get.return_value = mock_response
            
            # Should work with --repo skills
            result = fetch_resource(
                "anthropics",
                "test-skill",
                dest_path,
                ResourceType.SKILL,
                overwrite=False,
                repo="skills"
            )
            
            assert result.exists()
            assert result.name == "test-skill"
            content = (result / "SKILL.md").read_text()
            assert "Anthropics structure" in content


def test_opencode_pattern_detection():
    """Test pattern detection for opencode-style repos (skill/)"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        dest_path = tmp_path / "destination"
        
        # Create mock tarball with OpenCode structure
        tarball_bytes = create_mock_repo_tarball(tmp_path / "source", "codingagents", "opencode")
        
        # Mock httpx response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = tarball_bytes
        
        with patch('httpx.Client') as mock_client:
            mock_client.return_value.__enter__.return_value.get.return_value = mock_response
            
            # Should work with --repo codingagents
            result = fetch_resource(
                "opencode",
                "test-skill",
                dest_path,
                ResourceType.SKILL,
                overwrite=False,
                repo="codingagents"
            )
            
            assert result.exists()
            assert result.name == "test-skill"
            content = (result / "SKILL.md").read_text()
            assert "OpenCode structure" in content


def test_custom_destination():
    """Test custom destination path"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        custom_dest = tmp_path / "my-custom" / "location"
        
        # Create mock tarball
        tarball_bytes = create_mock_repo_tarball(tmp_path / "source", "agent-resources", "claude")
        
        # Mock httpx response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = tarball_bytes
        
        with patch('httpx.Client') as mock_client:
            mock_client.return_value.__enter__.return_value.get.return_value = mock_response
            
            # Should install to custom destination
            result = fetch_resource(
                "testuser",
                "test-skill",
                custom_dest,
                ResourceType.SKILL,
                overwrite=False,
                repo="agent-resources"
            )
            
            assert result.exists()
            assert str(custom_dest) in str(result)
            assert result.name == "test-skill"


def test_enhanced_error_messages():
    """Test that error messages show all attempted patterns"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        dest_path = tmp_path / "destination"
        
        # Create empty tarball (no resources)
        repo_dir = tmp_path / "source" / "agent-resources-main"
        repo_dir.mkdir(parents=True)
        
        tarball_path = tmp_path / "repo.tar.gz"
        with tarfile.open(tarball_path, "w:gz") as tar:
            tar.add(repo_dir, arcname="agent-resources-main")
        
        tarball_bytes = tarball_path.read_bytes()
        
        # Mock httpx response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = tarball_bytes
        
        with patch('httpx.Client') as mock_client:
            mock_client.return_value.__enter__.return_value.get.return_value = mock_response
            
            try:
                fetch_resource(
                    "testuser",
                    "nonexistent",
                    dest_path,
                    ResourceType.SKILL,
                    overwrite=False,
                    repo="agent-resources"
                )
                assert False, "Should have raised ResourceNotFoundError"
            except ResourceNotFoundError as e:
                error_msg = str(e)
                # Should show all attempted patterns
                assert "Tried these locations:" in error_msg
                assert ".claude/skills/nonexistent" in error_msg
                assert "skills/nonexistent" in error_msg
                assert "skill/nonexistent" in error_msg
                # Should show helpful suggestions
                assert "Quick fixes:" in error_msg
                assert "--repo" in error_msg
                assert "--dest" in error_msg


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
