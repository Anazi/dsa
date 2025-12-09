from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        """
        Count the number of islands in a 2D grid.

        An island is a group of '1's (land) connected horizontally or vertically.
        We find a '1', count it as a new island, and run DFS to
        'sink' (mark visited) the entire connected component.

        Time Complexity:  O(rows * cols)
            - Each cell is visited at most once.

        Space Complexity: O(rows * cols)
            - DFS recursion stack in worst case (grid is all '1').

        """

        # Edge case: empty grid
        if not grid:
            return 0

        rows = len(grid)
        cols = len(grid[0])
        islands = 0

        def dfs(r: int, c: int):
            """
            Perform DFS to mark the entire connected island as visited.

            We stop recursion when:
            - Coordinates go out of bounds
            - Cell is water ('0')
            - Cell is already visited ('0' after being marked)
            """

            # 1. Boundary check — outside the grid
            if r < 0 or r >= rows or c < 0 or c >= cols:
                return

            # 2. Stop if this is not land ('1')
            if grid[r][c] == '0':
                return

            # 3. Mark cell as visited (sink it)
            grid[r][c] = '0'

            # 4. Visit all 4 adjacent neighbors (up, down, left, right)
            dfs(r + 1, c)  # down
            dfs(r - 1, c)  # up
            dfs(r, c + 1)  # right
            dfs(r, c - 1)  # left

        # -------------------------------------------------------------

        # Scan every cell in the grid
        for r in range(rows):
            for c in range(cols):

                # If we find a '1', that means a NEW island
                if grid[r][c] == '1':
                    islands += 1  # Count this new island

                    # Run DFS to sink the entire island
                    dfs(r, c)

        return islands


# Example Test ----------------------------------------------
if __name__ == "__main__":
    grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"]
    ]

    sol = Solution()
    print(sol.numIslands(grid))  # Output: 3
