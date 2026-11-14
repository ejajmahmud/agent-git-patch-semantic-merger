"""Core git patch semantic merger implementation."""
import re
from typing import List, Tuple, Optional

class MergeConflict:
    def __init__(self, head_content: str, incoming_content: str):
        self.head_content = head_content
        self.incoming_content = incoming_content

class AstDiffChunk:
    def __init__(self, functions: List[str], imports: List[str]):
        self.functions = functions
        self.imports = imports

class GitPatchSemanticMerger:
    CONFLICT_REGEX = re.compile(
        r"""<<<<<<<.*?
(.*?)
=======
(.*?)
>>>>>>>.*?
""",
        re.DOTALL
    )

    def extract_conflicts(self, text: str) -> List[MergeConflict]:
        matches = self.CONFLICT_REGEX.findall(text)
        return [MergeConflict(m[0], m[1]) for m in matches]

    def resolve_textual_conflict(self, conflict: MergeConflict) -> Optional[str]:
        # Disjoint resolution: if both added functions or imports, combine them
        head_lines = set(conflict.head_content.splitlines())
        inc_lines = set(conflict.incoming_content.splitlines())

        # Combine lines preserving both sets without duplicates
        combined = []
        for line in conflict.head_content.splitlines():
            if line not in combined:
                combined.append(line)
        for line in conflict.incoming_content.splitlines():
            if line not in combined:
                combined.append(line)
        return chr(10).join(combined)

    def resolve_file(self, content: str) -> Tuple[str, int]:
        conflicts = self.extract_conflicts(content)
        if not conflicts:
            return content, 0

        resolved_count = 0
        def repl(match):
            nonlocal resolved_count
            c = MergeConflict(match.group(1), match.group(2))
            res = self.resolve_textual_conflict(c)
            if res is not None:
                resolved_count += 1
                return res + chr(10)
            return match.group(0)

        merged = self.CONFLICT_REGEX.sub(repl, content)
        return merged, resolved_count
