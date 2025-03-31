import os
import tempfile
from git import Repo
from tree_sitter import Language, Parser

class CodeIngestor:
    def __init__(self):
        self.supported_exts = {
            '.py': 'python',
            '.js': 'javascript',
            '.java': 'java',
            '.go': 'go'
        }
        self._init_parsers()

    def _init_parsers(self):
        """Build Tree-sitter parsers for each language"""
        self.parsers = {}
        for lang in self.supported_exts.values():
            Language.build_library(
                f'build/{lang}.so',
                [f'vendor/tree-sitter-{lang}']
            )
            self.parsers[lang] = Parser()
            self.parsers[lang].set_language(Language(f'build/{lang}.so', lang))

    def load_from_source(self, path):
        """Load from local directory"""
        return self._parse_files(path)

    def load_from_git(self, url, branch='main'):
        """Clone Git repo and parse files"""
        repo_path = tempfile.mkdtemp()
        Repo.clone_from(url, repo_path, branch=branch)
        return self._parse_files(repo_path)

    def _parse_files(self, path):
        """Extract code chunks with Tree-sitter"""
        code_chunks = []
        for root, _, files in os.walk(path):
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in self.supported_exts:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        code = f.read()
                    lang = self.supported_exts[ext]
                    tree = self.parsers[lang].parse(bytes(code, 'utf8'))
                    chunks = self._extract_functions(tree, code, lang)
                    code_chunks.extend(chunks)
        return code_chunks

    def _extract_functions(self, tree, code, lang):
        """Language-specific function extraction"""
        # Simplified - implement full query patterns per language
        if lang == 'python':
            return [f"Function in {lang}: {code.splitlines()[0]}"]
        return []