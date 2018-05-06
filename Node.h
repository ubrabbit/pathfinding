namespace PathFind
{
    /**
    * A node in the grid map
    */
    class Node
    {
    public:
        // node starting params
        bool walkable;
        int gridX;
        int gridY;
        float penalty;

        // calculated values while finding path
        int gCost;
        int hCost;
        Node* parent;

        // create the node
        // _price - how much does it cost to pass this tile. less is better, but 0.0f is for non-walkable.
        // _gridX, _gridY - tile location in grid.
        Node();
        Node(float _price, int _gridX, int _gridY);
        Node(const Node& b);
        ~Node();

        int fCost();

        bool operator ==(const Node b);
        bool operator !=(const Node b);
    };
}
