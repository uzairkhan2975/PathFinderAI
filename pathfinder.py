import os
import time
from rapidfuzz import fuzz

class PathFinderAI:
    def __init__(self, root="."):
        self.root = root

    def search(self, query, extensions=None, top_n=5):
        results = []
        for folder, _, files in os.walk(self.root):
            for file in files:
                if extensions and not any(file.endswith(ext) for ext in extensions):
                    continue
                filepath = os.path.join(folder, file)
                score = fuzz.partial_ratio(query.lower(), file.lower())
                results.append((score, filepath, os.path.getmtime(filepath)))

        # Sort by score, then time
        results.sort(key=lambda x: (-x[0], -x[2]))
        return results[:top_n]

# Example usage
if __name__ == "__main__":
    pf = PathFinderAI(root=".")
    results = pf.search("api script", extensions=[".py"])
    for score, path, mtime in results:
        print(f"[{score}%] {path} (Last modified: {time.ctime(mtime)})")
