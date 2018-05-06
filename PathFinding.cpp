#include "PathFinding.h"

#include <iostream>
#include <cmath>
#include <set>
#include <map>

#include "Grid.h"
#include "Point.h"
#include "Node.h"

using namespace std;

namespace PathFind
{
    list<Point> Pathfinding::FindPath(Grid grid, Point startPos, Point targetPos)
    {
        // convert to a list of points and return
        list<Point> ret;
        if (startPos.x < 0 || startPos.x >= grid.gridSizeX || startPos.y < 0 || startPos.y >= grid.gridSizeY)
        {
            return ret;
        }

        // find path
        ret = _ImpFindPath(grid, startPos, targetPos);
        return ret;
    }

    list<Point> Pathfinding::_ImpFindPath(Grid grid, Point startPos, Point targetPos)
    {
        Node startNode = grid.GetNode(startPos.x, startPos.y);
        Node targetNode = grid.GetNode(targetPos.x, targetPos.y);

        list<Node> openSet;

        int closedSet[grid.gridSizeX][grid.gridSizeY] = {0};
        Node parentSet[grid.gridSizeX][grid.gridSizeY];
        Node emptyNode = Node();
        for(int i=0; i<grid.gridSizeX; i++)
        {
            for(int j=0; j<grid.gridSizeY; j++)
            {
                closedSet[i][j] = 0;
                parentSet[i][j] = emptyNode;
            }
        }

        bool is_find = false;
        openSet.push_back( startNode );
        while (openSet.size() > 0)
        {
            list<Node>::iterator iterNode = openSet.begin();
            Node currentNode = *iterNode;

            for( list<Node>::iterator iter=iterNode; iter!=openSet.end(); iter++ )
            {
                Node tmpNode = *iter;
                if ( tmpNode.fCost() < currentNode.fCost() || (tmpNode.fCost() == currentNode.fCost() && tmpNode.hCost < currentNode.hCost) )
                {
                    iterNode = iter;
                    currentNode = tmpNode;
                }
            }
            openSet.erase( iterNode );
            closedSet[currentNode.gridX][currentNode.gridY] = 1;

            if (currentNode == targetNode)
            {
                targetNode = currentNode;
                is_find = true;
                break;
            }

            list<Node> neighbour_set = grid.GetNeighbours(currentNode);
            for( list<Node>::iterator iter=neighbour_set.begin(); iter!=neighbour_set.end(); iter++ )
            {
                Node neighbour = *iter;
                int x = neighbour.gridX;
                int y = neighbour.gridY;
                if (!neighbour.walkable || (closedSet[x][y]==1) )
                {
                    continue;
                }

                int newMovementCostToNeighbour = currentNode.gCost + GetDistance(currentNode, neighbour) * (int)(10.0f * neighbour.penalty);
                if ( (newMovementCostToNeighbour < neighbour.gCost) || (parentSet[x][y] == emptyNode) )
                {
                    neighbour.gCost = newMovementCostToNeighbour;
                    neighbour.hCost = GetDistance(neighbour, targetNode);

                    if ( parentSet[x][y] == emptyNode )
                    {
                        openSet.push_back(neighbour);
                        parentSet[x][y] = currentNode;
                    }
                }
            }
        }

        list<Point> pointList;
        if ( is_find )
        {
            Node tmpNode = targetNode;
            while (tmpNode != startNode)
            {
                pointList.push_back( Point(tmpNode.gridX, tmpNode.gridY) );
                tmpNode = parentSet[tmpNode.gridX][tmpNode.gridY];
            }
            pointList.reverse();
        }
        return pointList;
    }

    int Pathfinding::GetDistance(Node nodeA, Node nodeB)
    {
        int dstX = fabs(nodeA.gridX - nodeB.gridX);
        int dstY = fabs(nodeA.gridY - nodeB.gridY);

        if (dstX > dstY)
            return 14 * dstY + 10 * (dstX - dstY);
        return 14 * dstX + 10 * (dstY - dstX);
    }

}
