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
        list<Node> nodes_path = _ImpFindPath(grid, startPos, targetPos);
        for( list<Node>::iterator iter=nodes_path.begin(); iter!=nodes_path.end(); iter++ )
        {
            ret.push_back( Point((*iter).gridX, (*iter).gridY) );
        }
        return ret;
    }

    list<Node> Pathfinding::_ImpFindPath(Grid grid, Point startPos, Point targetPos)
    {
            Node startNode = grid.GetNode(startPos.x, startPos.y);
            Node targetNode = grid.GetNode(targetPos.x, targetPos.y);

            list<Node*> nodeList;
            list<Node> openSet;

            int closedSet[grid.gridSizeX][grid.gridSizeY] = {0};
            int historySet[grid.gridSizeX][grid.gridSizeY] = {0};
            for(int i=0; i<grid.gridSizeX; i++)
            {
                for(int j=0; j<grid.gridSizeY; j++)
                {
                    closedSet[i][j] = 0;
                    historySet[i][j] = 0;
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

                //cout<<"currentNode:   "<<currentNode.gridX<<","<<currentNode.gridY<<endl;
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
                        //cout<<"neighbour00:   "<<x<<","<<y<<"   : "<<closedSet[x][y]<<"   :  "<<neighbour.walkable<<endl;
                        continue;
                    }

                    int newMovementCostToNeighbour = currentNode.gCost + GetDistance(currentNode, neighbour) * (int)(10.0f * neighbour.penalty);
                    //cout<<"neighbour11:   "<<x<<","<<y<<"   : "<<newMovementCostToNeighbour<<"   :  "<<neighbour.gCost<<": "<<historySet[x][y]<<endl;
                    if (newMovementCostToNeighbour < neighbour.gCost || historySet[x][y]==0 )
                    {
                        Node* copyNode = new Node(currentNode);
                        nodeList.push_back( copyNode );

                        neighbour.gCost = newMovementCostToNeighbour;
                        neighbour.hCost = GetDistance(neighbour, targetNode);
                        neighbour.parent = copyNode;

                        //cout<<"neighbour22:   "<<x<<","<<y<<"   : "<<historySet[x][y]<<endl;
                        if (historySet[x][y]==0)
                        {
                            openSet.push_back(neighbour);
                            historySet[x][y] = 1;
                        }
                    }
                }
            }

            list<Node> pathList;
            if ( is_find )
            {
                Node tmpNode = targetNode;
                while (tmpNode != startNode)
                {
                    pathList.push_back(tmpNode);
                    tmpNode = *(tmpNode.parent);
                }
                pathList.reverse();
            }
            for( list<Node*>::iterator iter=nodeList.begin(); iter!=nodeList.end(); iter++ )
            {
                delete (*iter);
            }
            nodeList.clear();
            return pathList;
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
