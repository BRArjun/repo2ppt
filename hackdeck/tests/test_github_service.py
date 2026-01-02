import pytest
from pathlib import Path
from app.services.github_service import GitHubService


class TestGitHubService:
    """Test cases for GitHub service"""
    
    @pytest.fixture
    def github_service(self):
        """Create GitHub service instance"""
        return GitHubService()
    
    def test_clone_valid_repository(self, github_service):
        """Test cloning a valid public repository"""
        # Using a small test repo
        test_url = "https://github.com/octocat/Hello-World"
        
        repo_path = github_service.clone_repository(test_url)
        
        assert repo_path.exists()
        assert repo_path.is_dir()
        assert (repo_path / ".git").exists()
        
        # Cleanup
        github_service.cleanup_repository(repo_path)
    
    def test_clone_invalid_repository(self, github_service):
        """Test cloning an invalid repository"""
        test_url = "https://github.com/invalid/repo-does-not-exist-12345"
        
        with pytest.raises(Exception) as exc_info:
            github_service.clone_repository(test_url)
        
        assert "Failed to clone repository" in str(exc_info.value)
    
    def test_clone_non_github_url(self, github_service):
        """Test that non-GitHub URLs are rejected by validator"""
        # This should be caught by the validator before reaching the service
        test_url = "https://gitlab.com/user/repo"
        
        # The validator should catch this, but if it reaches the service:
        with pytest.raises(Exception):
            github_service.clone_repository(test_url)
    
    def test_cleanup_repository(self, github_service, tmp_path):
        """Test repository cleanup"""
        # Create a temporary directory
        test_dir = tmp_path / "test_repo"
        test_dir.mkdir()
        (test_dir / "test_file.txt").write_text("test")
        
        github_service.cleanup_repository(test_dir)
        
        assert not test_dir.exists()
    
    def test_cleanup_nonexistent_directory(self, github_service, tmp_path):
        """Test cleanup of non-existent directory doesn't raise error"""
        non_existent = tmp_path / "does_not_exist"
        
        # Should not raise an exception
        github_service.cleanup_repository(non_existent)
    
    def test_get_directory_size(self, github_service, tmp_path):
        """Test directory size calculation"""
        test_dir = tmp_path / "test_size"
        test_dir.mkdir()
        
        # Create files of known size
        (test_dir / "file1.txt").write_text("a" * 1024)  # 1KB
        (test_dir / "file2.txt").write_text("b" * 1024)  # 1KB
        
        size_mb = github_service._get_directory_size(test_dir)
        
        # Should be approximately 0.002 MB (2KB)
        assert 0.001 < size_mb < 0.01


class TestGitHubServiceIntegration:
    """Integration tests for GitHub service"""
    
    @pytest.fixture
    def github_service(self):
        return GitHubService()
    
    @pytest.mark.slow
    def test_full_clone_and_cleanup_workflow(self, github_service):
        """Test complete workflow: clone -> verify -> cleanup"""
        test_url = "https://github.com/octocat/Hello-World"
        
        # Clone
        repo_path = github_service.clone_repository(test_url)
        assert repo_path.exists()
        
        # Verify structure
        assert (repo_path / "README").exists() or (repo_path / "README.md").exists()
        
        # Cleanup
        github_service.cleanup_repository(repo_path)
        assert not repo_path.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])