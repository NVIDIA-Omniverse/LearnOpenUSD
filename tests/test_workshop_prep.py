"""Tests for the lousd.workshop_prep module.

This module tests the workshop preparation script's functionality, including:
- Path resolution for cross-references
- Conversion of {doc} references to external links
- Conversion of markdown links to external links
- Validation that generated external URLs are accessible
"""

import re
from pathlib import Path

import pytest
import requests

from lousd.workshop_prep import (
    EXTERNAL_BASE_URL,
    FILES_TO_REMOVE,
    MODULES_TO_KEEP,
    MODULES_TO_REMOVE,
    convert_doc_reference,
    convert_markdown_link,
    resolve_doc_reference_path,
)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def temp_docs_dir(tmp_path: Path) -> Path:
    """Create a temporary docs directory structure for testing.

    Args:
        tmp_path: Pytest's temporary path fixture.

    Returns:
        Path to the temporary docs directory.
    """
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

    # Create some module directories
    for module in MODULES_TO_REMOVE + MODULES_TO_KEEP:
        module_dir = docs_dir / module
        module_dir.mkdir()
        (module_dir / "index.md").write_text(f"# {module}\n")

    # Create a test file in a kept module
    test_file = docs_dir / "asset-structure" / "test.md"
    test_file.write_text("# Test file\n")

    return docs_dir


@pytest.fixture
def sample_current_file(temp_docs_dir: Path) -> Path:
    """Return a sample current file path for testing.

    Args:
        temp_docs_dir: Temporary docs directory fixture.

    Returns:
        Path to a sample file in the asset-structure module.
    """
    return temp_docs_dir / "asset-structure" / "test.md"


# =============================================================================
# Tests for module constants
# =============================================================================


class TestModuleConstants:
    """Tests for module-level constants."""

    def test_modules_to_keep_not_empty(self) -> None:
        """Verify MODULES_TO_KEEP contains expected modules."""
        assert len(MODULES_TO_KEEP) > 0
        assert "creating-composition-arcs" in MODULES_TO_KEEP
        assert "asset-structure" in MODULES_TO_KEEP
        assert "data-exchange" in MODULES_TO_KEEP
        assert "asset-modularity-instancing" in MODULES_TO_KEEP

    def test_modules_to_remove_not_empty(self) -> None:
        """Verify MODULES_TO_REMOVE contains expected modules."""
        assert len(MODULES_TO_REMOVE) > 0
        assert "stage-setting" in MODULES_TO_REMOVE
        assert "beyond-basics" in MODULES_TO_REMOVE

    def test_no_overlap_between_keep_and_remove(self) -> None:
        """Verify no module appears in both keep and remove lists."""
        keep_set = set(MODULES_TO_KEEP)
        remove_set = set(MODULES_TO_REMOVE)
        overlap = keep_set & remove_set
        assert len(overlap) == 0, f"Modules in both lists: {overlap}"

    def test_external_base_url_format(self) -> None:
        """Verify EXTERNAL_BASE_URL has correct format."""
        assert EXTERNAL_BASE_URL.startswith("https://")
        assert EXTERNAL_BASE_URL.endswith("/")
        assert "docs.nvidia.com" in EXTERNAL_BASE_URL


# =============================================================================
# Tests for resolve_doc_reference_path
# =============================================================================


class TestResolveDocReferencePath:
    """Tests for the resolve_doc_reference_path function."""

    def test_relative_path_to_removed_module(
        self, temp_docs_dir: Path, sample_current_file: Path
    ) -> None:
        """Test resolving a relative path that points to a removed module."""
        ref_path = "../stage-setting/index.md"
        result = resolve_doc_reference_path(ref_path, sample_current_file, temp_docs_dir)
        assert result is not None
        assert result.startswith("stage-setting")

    def test_relative_path_to_kept_module(
        self, temp_docs_dir: Path, sample_current_file: Path
    ) -> None:
        """Test resolving a relative path that points to a kept module."""
        ref_path = "../creating-composition-arcs/index.md"
        result = resolve_doc_reference_path(ref_path, sample_current_file, temp_docs_dir)
        assert result is None  # Should not be converted

    def test_dot_slash_path_to_removed_module(
        self, temp_docs_dir: Path
    ) -> None:
        """Test resolving a ./ path that points to a removed module."""
        # File at docs root
        current_file = temp_docs_dir / "glossary.md"
        current_file.write_text("# Glossary\n")

        ref_path = "beyond-basics/value-resolution.md"
        result = resolve_doc_reference_path(ref_path, current_file, temp_docs_dir)
        assert result is not None
        assert "beyond-basics" in result

    def test_absolute_path_to_removed_module(
        self, temp_docs_dir: Path, sample_current_file: Path
    ) -> None:
        """Test resolving an absolute path that points to a removed module."""
        ref_path = "/composition-basics/layers.md"
        result = resolve_doc_reference_path(ref_path, sample_current_file, temp_docs_dir)
        assert result is not None
        assert result.startswith("composition-basics")

    def test_path_to_removed_file(
        self, temp_docs_dir: Path, sample_current_file: Path
    ) -> None:
        """Test resolving a path that points to a removed individual file."""
        # Create the file
        (temp_docs_dir / "usdview-install-instructions.md").write_text("# Install\n")

        ref_path = "../usdview-install-instructions.md"
        result = resolve_doc_reference_path(ref_path, sample_current_file, temp_docs_dir)
        assert result is not None
        assert "usdview-install-instructions" in result

    def test_path_to_setup_page_in_kept_module(
        self, temp_docs_dir: Path, sample_current_file: Path
    ) -> None:
        """Test resolving a path to a setup page in a kept module."""
        ref_path = "setup.md"
        result = resolve_doc_reference_path(ref_path, sample_current_file, temp_docs_dir)
        assert result is not None
        assert "setup" in result


# =============================================================================
# Tests for convert_doc_reference
# =============================================================================


class TestConvertDocReference:
    """Tests for the convert_doc_reference function."""

    def test_convert_simple_doc_reference(
        self, temp_docs_dir: Path, sample_current_file: Path
    ) -> None:
        """Test converting a simple {doc} reference."""
        pattern = re.compile(r'\{doc\}`([^`]+)`')
        text = "{doc}`../stage-setting/index`"
        match = pattern.match(text)
        assert match is not None

        result = convert_doc_reference(match, sample_current_file, temp_docs_dir)
        assert result.startswith("[")
        assert EXTERNAL_BASE_URL in result
        assert ".html" in result

    def test_convert_labeled_doc_reference(
        self, temp_docs_dir: Path, sample_current_file: Path
    ) -> None:
        """Test converting a labeled {doc} reference."""
        pattern = re.compile(r'\{doc\}`([^`]+)`')
        text = "{doc}`My Custom Label <../beyond-basics/hydra>`"
        match = pattern.match(text)
        assert match is not None

        result = convert_doc_reference(match, sample_current_file, temp_docs_dir)
        assert "[My Custom Label]" in result
        assert EXTERNAL_BASE_URL in result

    def test_preserve_doc_reference_to_kept_module(
        self, temp_docs_dir: Path, sample_current_file: Path
    ) -> None:
        """Test that {doc} references to kept modules are preserved."""
        pattern = re.compile(r'\{doc\}`([^`]+)`')
        text = "{doc}`../data-exchange/index`"
        match = pattern.match(text)
        assert match is not None

        result = convert_doc_reference(match, sample_current_file, temp_docs_dir)
        # Should return original since data-exchange is kept
        assert result == text


# =============================================================================
# Tests for convert_markdown_link
# =============================================================================


class TestConvertMarkdownLink:
    """Tests for the convert_markdown_link function."""

    def test_convert_simple_markdown_link(
        self, temp_docs_dir: Path, sample_current_file: Path
    ) -> None:
        """Test converting a simple markdown link."""
        pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        text = "[Setting the Stage](../stage-setting/index.md)"
        match = pattern.match(text)
        assert match is not None

        result = convert_markdown_link(match, sample_current_file, temp_docs_dir)
        assert "[Setting the Stage]" in result
        assert EXTERNAL_BASE_URL in result
        assert ".html" in result

    def test_convert_angle_bracket_link(
        self, temp_docs_dir: Path
    ) -> None:
        """Test converting a MyST angle bracket syntax link."""
        current_file = temp_docs_dir / "glossary.md"
        current_file.write_text("# Glossary\n")

        pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        text = "[Active Prims](<beyond-basics/active-inactive-prims.md>)"
        match = pattern.match(text)
        assert match is not None

        result = convert_markdown_link(match, current_file, temp_docs_dir)
        assert "[Active Prims]" in result
        assert EXTERNAL_BASE_URL in result
        # Angle brackets should be stripped
        assert "<" not in result.split("](")[1]

    def test_preserve_external_links(
        self, temp_docs_dir: Path, sample_current_file: Path
    ) -> None:
        """Test that external links are preserved."""
        pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        text = "[OpenUSD](https://openusd.org)"
        match = pattern.match(text)
        assert match is not None

        result = convert_markdown_link(match, sample_current_file, temp_docs_dir)
        assert result == text

    def test_preserve_anchor_only_links(
        self, temp_docs_dir: Path, sample_current_file: Path
    ) -> None:
        """Test that anchor-only links are preserved."""
        pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        text = "[Jump to section](#my-section)"
        match = pattern.match(text)
        assert match is not None

        result = convert_markdown_link(match, sample_current_file, temp_docs_dir)
        assert result == text

    def test_preserve_intersphinx_links(
        self, temp_docs_dir: Path, sample_current_file: Path
    ) -> None:
        """Test that intersphinx links are preserved."""
        pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        text = "[USD Glossary](<inv:usd:std#glossary:stage>)"
        match = pattern.match(text)
        assert match is not None

        result = convert_markdown_link(match, sample_current_file, temp_docs_dir)
        assert result == text

    def test_preserve_anchor_in_external_link(
        self, temp_docs_dir: Path, sample_current_file: Path
    ) -> None:
        """Test that anchors are preserved when converting links."""
        pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        text = "[Value Resolution](../beyond-basics/value-resolution.md#fallback-values)"
        match = pattern.match(text)
        assert match is not None

        result = convert_markdown_link(match, sample_current_file, temp_docs_dir)
        assert "#fallback-values" in result
        assert EXTERNAL_BASE_URL in result


# =============================================================================
# Tests for external URL validation
# =============================================================================


class TestExternalURLValidation:
    """Tests that verify generated external URLs are accessible."""

    # Sample URLs that should exist on the live documentation site
    SAMPLE_URLS = [
        "stage-setting/index.html",
        "beyond-basics/index.html",
        "composition-basics/index.html",
        "stage-setting/prims.html",
        "beyond-basics/value-resolution.html",
        "glossary.html",
    ]

    @pytest.mark.parametrize("path", SAMPLE_URLS)
    def test_external_url_is_accessible(self, path: str) -> None:
        """Test that sample external URLs return successful responses.

        Args:
            path: The path portion of the URL to test.
        """
        url = EXTERNAL_BASE_URL + path
        try:
            response = requests.head(url, allow_redirects=True, timeout=10.0)
            assert response.status_code == 200, f"URL {url} returned {response.status_code}"
        except requests.exceptions.RequestException as e:
            pytest.skip(f"Could not connect to {url}: {e}")

    def test_base_url_is_accessible(self) -> None:
        """Test that the base documentation URL is accessible."""
        try:
            response = requests.head(EXTERNAL_BASE_URL, allow_redirects=True, timeout=10.0)
            assert response.status_code == 200
        except requests.exceptions.RequestException as e:
            pytest.skip(f"Could not connect to {EXTERNAL_BASE_URL}: {e}")

    def test_removed_module_urls_pattern(self) -> None:
        """Test that URLs for all removed modules follow the expected pattern."""
        for module in MODULES_TO_REMOVE:
            url = f"{EXTERNAL_BASE_URL}{module}/index.html"
            try:
                response = requests.head(url, allow_redirects=True, timeout=10.0)
                # We expect these to exist on the live site
                assert response.status_code == 200, (
                    f"Removed module URL {url} should exist but returned {response.status_code}"
                )
            except requests.exceptions.RequestException as e:
                pytest.skip(f"Could not connect to {url}: {e}")


# =============================================================================
# Integration tests
# =============================================================================


class TestIntegration:
    """Integration tests for the workshop_prep module."""

    def test_full_conversion_pipeline(self, temp_docs_dir: Path) -> None:
        """Test the full conversion of a file with multiple reference types."""
        # Create a test file with various reference types
        test_content = """# Test Page

See the {doc}`stage lesson <../stage-setting/index>` for more info.

Also check out:
- [Beyond Basics](../beyond-basics/index.md)
- [Value Resolution](../beyond-basics/value-resolution.md#section)
- [External Link](https://example.com)
- [Kept Module](../data-exchange/index.md)

Further reading: [Prims](<../stage-setting/prims.md>)
"""
        test_file = temp_docs_dir / "asset-structure" / "test-page.md"
        test_file.write_text(test_content)

        # Apply conversions
        doc_pattern = re.compile(r'\{doc\}`([^`]+)`')
        md_link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

        content = test_file.read_text()

        content = doc_pattern.sub(
            lambda m: convert_doc_reference(m, test_file, temp_docs_dir),
            content
        )
        content = md_link_pattern.sub(
            lambda m: convert_markdown_link(m, test_file, temp_docs_dir),
            content
        )

        # Verify conversions
        assert EXTERNAL_BASE_URL in content  # Some links converted
        assert "https://example.com" in content  # External link preserved
        assert "../data-exchange/index.md" in content  # Kept module preserved
        assert "#section" in content  # Anchor preserved

        # Count external URLs - should have converted stage-setting and beyond-basics refs
        external_count = content.count(EXTERNAL_BASE_URL)
        assert external_count >= 3, f"Expected at least 3 external URLs, found {external_count}"


# =============================================================================
# Full integration tests - runs workshop_prep on real docs copy
# =============================================================================


@pytest.fixture(scope="class")
def docs_copy(tmp_path_factory) -> Path:
    """Create a copy of docs and run workshop_prep on it once for all tests.
    
    Args:
        tmp_path_factory: Pytest's session-scoped temporary path factory.
    
    Returns:
        Path to the processed docs directory.
    """
    import shutil
    from lousd import workshop_prep
    
    # Get the real docs directory
    real_docs = Path(__file__).parent.parent / "docs"
    
    # Copy to temp location, ignoring build artifacts
    temp_dir = tmp_path_factory.mktemp("workshop_test")
    docs_copy = temp_dir / "docs"
    shutil.copytree(
        real_docs,
        docs_copy,
        symlinks=True,
        ignore=shutil.ignore_patterns("_build", "__pycache__", "*.pyc")
    )
    
    # Run workshop_prep once
    workshop_prep.main(docs_dir=docs_copy)
    
    return docs_copy


class TestWorkshopPrepIntegration:
    """Integration tests that validate workshop_prep results on a real docs copy."""

    def test_site_title_updated(self, docs_copy: Path) -> None:
        """Verify workshop_prep updated conf.py with the workshop title."""
        conf_path = docs_copy / "conf.py"
        content = conf_path.read_text(encoding="utf-8")
        assert "Learn OpenUSD: Applied Concepts Workshop" in content

    def test_main_index_transformed(self, docs_copy: Path) -> None:
        """Verify workshop_prep transformed index.md for the workshop."""
        index_path = docs_copy / "index.md"
        content = index_path.read_text(encoding="utf-8")
        
        # Should have workshop title
        assert "Learn OpenUSD: Applied Concepts Workshop" in content
        
        # Should have the 2x2 grid of module cards
        assert "grid-item-card" in content
        assert "Start Learning" in content
        
        # Should reference all kept modules
        for module in MODULES_TO_KEEP:
            assert module in content
        
        # Should have Common Resources section
        assert "Common Resources" in content
        assert "why-openusd-developer-certification" in content

    def test_removed_modules_deleted(self, docs_copy: Path) -> None:
        """Verify workshop_prep removed the correct module directories."""
        # Verify removed modules are gone
        for module in MODULES_TO_REMOVE:
            module_path = docs_copy / module
            assert not module_path.exists(), f"{module} should be removed"
        
        # Verify kept modules still exist
        for module in MODULES_TO_KEEP:
            module_path = docs_copy / module
            assert module_path.exists(), f"{module} should still exist"

    def test_removed_files_deleted(self, docs_copy: Path) -> None:
        """Verify workshop_prep removed individual files."""
        for filename in FILES_TO_REMOVE:
            file_path = docs_copy / filename
            assert not file_path.exists(), f"{filename} should be removed"

    def test_setup_pages_removed(self, docs_copy: Path) -> None:
        """Verify workshop_prep removed setup.md files from kept modules."""
        for module in MODULES_TO_KEEP:
            setup_path = docs_copy / module / "setup.md"
            assert not setup_path.exists(), f"Setup page in {module} should be removed"
            
            # Verify index no longer references setup
            index_path = docs_copy / module / "index.md"
            if index_path.exists():
                content = index_path.read_text(encoding="utf-8")
                assert "Setup <setup>" not in content

    def test_cross_references_converted(self, docs_copy: Path) -> None:
        """Verify workshop_prep converted cross-references to external links."""
        glossary_path = docs_copy / "glossary.md"
        
        if not glossary_path.exists():
            pytest.skip("glossary.md not found")
        
        content = glossary_path.read_text(encoding="utf-8")
        
        # Should have some external links now
        assert EXTERNAL_BASE_URL in content, "Glossary should have external links"
        
        # Should not have unconverted relative links to removed modules
        for module in MODULES_TO_REMOVE:
            # Pattern for relative markdown links
            bad_pattern = f"]({module}/"
            if bad_pattern in content:
                # Make sure it's part of an external URL
                assert EXTERNAL_BASE_URL in content.split(bad_pattern)[0].split("\n")[-1]

    def test_kept_modules_preserved(self, docs_copy: Path) -> None:
        """Verify all kept modules and their content are preserved."""
        for module in MODULES_TO_KEEP:
            module_path = docs_copy / module
            assert module_path.exists(), f"Kept module {module} should exist"
            
            # Verify index exists
            index_path = module_path / "index.md"
            assert index_path.exists(), f"Index for {module} should exist"

    def test_certification_page_preserved(self, docs_copy: Path) -> None:
        """Verify the certification page is preserved."""
        cert_page = docs_copy / "why-openusd-developer-certification.md"
        assert cert_page.exists(), "Certification page should be preserved"

    def test_glossary_pages_preserved(self, docs_copy: Path) -> None:
        """Verify glossary pages are preserved."""
        assert (docs_copy / "glossary.md").exists(), "glossary.md should be preserved"
        assert (docs_copy / "interactive-glossary.md").exists(), "interactive-glossary.md should be preserved"
