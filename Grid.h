#include <vector>
#include <list>

namespace PathFind
{
    class Node;

    /**
    * The grid of nodes we use to find path
    */
    class Grid
    {
    public:
        int gridSizeX, gridSizeY;

        /**
        * Create a new grid with tile prices.
        * width: grid width.
        * height: grid height.
        * tiles_costs: 2d array of floats, representing the cost of every tile.
        *               0.0f = unwalkable tile.
        *               1.0f = normal tile.
        */
        Grid(int width, int height, std::vector< std::vector<float> > tiles_costs);

        /**
        * Create a new grid of just walkable / unwalkable.
        * width: grid width.
        * height: grid height.
        * walkable_tiles: the tilemap. true for walkable, false for blocking.
        */
        Grid(int width, int height, std::vector< std::vector<bool> > walkable_tiles);
        Grid(const Grid& g);

        ~Grid();

        std::list<Node> GetNeighbours(Node node);
        Node GetNode(int x, int y);
        bool SetNodeCost(int x, int y, int cost, bool walkable);

        void DebugPrint();
        void DebugPrintList(std::list<Node> nodeList);

    private:
        std::vector< std::vector<Node> > nodes;
    };
}
