# Sudoku Solver (Logic-Only)

## Overview
This Python project implements a **logic-based Sudoku solver** without resorting to brute-force guessing or trial-and-error.  
The solver is designed to mimic human solving techniques, applying them in iterative passes until the grid is solved.

The current implementation handles:
- **Basic elimination** by row, column, and box
- **Single candidate detection** (naked singles)
- **Reserved spots** (simple naked subsets detection)

The code is built around a `Space` class representing each cell, with methods for reducing candidate possibilities based on Sudoku constraints.

---

## Current Techniques Implemented

### 1. Row/Column/Box Elimination
Removes candidates from a cell if they already exist in the same row, column, or 3×3 box.

### 2. Naked Singles
If a cell has only one possible candidate, it is assigned directly.

### 3. Reserved Spots (Basic Naked Subsets)
If a group of N cells in the same row, column, or box shares exactly the same N candidates, these candidates can be eliminated from other cells in the group.

---

## Planned Techniques

The following logical strategies are planned for future implementation:

### 4. Extended Naked Subsets
Generalize "reserved spots" to handle naked pairs, triples, and quadruples where candidates may be subsets, not just identical lists.

### 5. Hidden Subsets (Pairs/Triples/Quads)
Detect cases where an exact set of N candidates appears in exactly N cells of a group, even if those cells have other candidates.  
**Example:** Hidden pair `{2,3}` in a row appears only in two cells — remove other candidates from those cells.

### 6. Box-Line Reduction (Pointing Pairs/Triples)
When a candidate is confined to one row or column inside a 3×3 box, remove it from the rest of that row or column.

### 7. X-Wing
A candidate that appears in exactly two cells in two different rows and aligned in the same columns allows elimination of that candidate from other cells in those columns.

### 8. Swordfish
Generalization of X-Wing for three rows and columns.

---

## Design Philosophy
- **No backtracking**: The solver will **never guess**; it must rely entirely on logical deductions.
- **Readable logic flow**: Techniques should be implemented as clear, testable functions.
- **Step-by-step processing**: Apply techniques in passes, starting from simplest to most complex.
- **Traceability**: Potential for a "verbose mode" to log each logical deduction for debugging and learning purposes.

---

## Roadmap
1. Refactor existing `reserved_spots` to use sets for cleaner subset detection.
2. Implement **hidden subsets** logic using candidate frequency mapping.
3. Add **box-line reduction** for candidate elimination across intersecting groups.
4. Integrate **X-Wing** and **Swordfish** pattern recognition.
5. Implement a **color system** to distinguish start and solution.

---

## License
MIT License
