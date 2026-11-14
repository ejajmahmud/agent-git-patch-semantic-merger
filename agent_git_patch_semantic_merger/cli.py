"""CLI for agent-git-patch-semantic-merger."""
import argparse
import sys
from .core import GitPatchSemanticMerger

def main():
    parser = argparse.ArgumentParser(description="Agent Git Patch Semantic Merger CLI")
    parser.add_argument("--demo", action="store_true", help="Run git patch semantic merge demo")
    args = parser.parse_args()

    if args.demo:
        merger = GitPatchSemanticMerger()
        conflict_code = """import os
<<<<<<< HEAD
def feature_alpha():
    return "alpha"
=======
def feature_beta():
    return "beta"
>>>>>>> incoming_branch
"""
        clean_code, count = merger.resolve_file(conflict_code)
        print(f"[+] Resolved {count} merge conflicts automatically:")
        print(clean_code)
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
