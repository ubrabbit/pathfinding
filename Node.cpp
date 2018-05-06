#include "Node.h"

namespace PathFind
{
    Node::Node()
    {
        gCost = 0;
        hCost = 0;
        walkable = false;
        penalty = 0.0f;
        gridX = -1;
        gridY = -1;
    }

    Node::Node(float _price, int _gridX, int _gridY)
    {
        gCost = 0;
        hCost = 0;
        walkable = _price != 0.0f;
        penalty = _price;
        gridX = _gridX;
        gridY = _gridY;
    }

    Node::Node(const Node& b)
    {
        walkable = b.walkable;
        penalty = b.penalty;
        gridX = b.gridX;
        gridY = b.gridY;
        gCost = b.gCost;
        hCost = b.hCost;
    }

    int Node::fCost()
    {
        return gCost + hCost;
    }

    bool Node::operator ==(const Node b)
    {
        return (gridX == b.gridX) && (gridY == b.gridY);
    }

    bool Node::operator !=(const Node b)
    {
        return !( (*this) == b );
    }

}
