#include <vector>
#include <list>
#include <map>

namespace PathFind
{
    class Grid;
    class Point;
    class Node;

    /**
    * Main class to find the best path from A to B.
    * Use like this:
    * Grid grid = new Grid(width, height, tiles_costs);
    * List<Point> path = Pathfinding.FindPath(grid, from, to);
    */
    class Pathfinding
    {
    public:
        // The API you should use to get path
        // grid: grid to search in.
        // startPos: starting position.
        // targetPos: ending position.
        static std::list<Point> FindPath(Grid grid, Point startPos, Point targetPos);

    private:
        // internal function to find path, don't use this one from outside
        static std::list<Node> _ImpFindPath(Grid grid, Point startPos, Point targetPos);
        static int GetDistance(Node nodeA, Node nodeB);
    };

}
