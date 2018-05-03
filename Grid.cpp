#include "Grid.h"
#include "Node.h"

#include <iostream>

namespace PathFind
{
    using namespace std;

    Grid::Grid(int width, int height, vector<float> tiles_costs)
    {
        gridSizeX = width;
        gridSizeY = height;

        for (int x = 0; x < width; x++)
        {
            for (int y = 0; y < height; y++)
            {
                nodes.push_back( Node(tiles_costs[ x * width + y ], x, y) );
            }
        }
    }

    Grid::Grid(int width, int height, vector<bool> walkable_tiles)
    {
        gridSizeX = width;
        gridSizeY = height;

        for (int x = 0; x < width; x++)
        {
            for (int y = 0; y < height; y++)
            {
                nodes.push_back( Node(walkable_tiles[ x * width + y ] ? 1.0f : 0.0f, x, y) );
            }
        }
    }

    Grid::Grid(const Grid& g)
    {
        gridSizeX = g.gridSizeX;
        gridSizeY = g.gridSizeY;
        nodes = g.nodes;
    }

    Grid::~Grid()
    {
        nodes.clear();
    }

    list<Node> Grid::GetNeighbours(Node node)
    {
        list<Node> neighbours;

        for (int x = -1; x <= 1; x++)
        {
            for (int y = -1; y <= 1; y++)
            {
                if (x == 0 && y == 0)
                    continue;

                int checkX = node.gridX + x;
                int checkY = node.gridY + y;

                if (checkX >= 0 && checkX < gridSizeX && checkY >= 0 && checkY < gridSizeY)
                {
                    neighbours.push_back( nodes[ checkX * gridSizeX + checkY ] );
                }
            }
        }

        return neighbours;
    }

    Node Grid::GetNode(int x, int y)
    {
        return nodes[ x * gridSizeX + y ];
    }

    bool Grid::SetNodeCost(int x, int y, int cost, bool walkable)
    {
        if( x >= gridSizeX ) return false;
        if( y >= gridSizeY ) return false;

        //cout<<"SetNodeCost:  "<<x<<","<<y<<"  "<<cost<<" "<<walkable<<endl;
        nodes[ x * gridSizeX + y ].penalty = (float)cost;
        nodes[ x * gridSizeX + y ].walkable = walkable;
        return true;
    }

    void Grid::DebugPrint()
    {
        cout<<">>>>>>>>>>>>>>>>>>> costs: "<<endl;
        for(int i=0; i<gridSizeX; i++)
        {
            for(int j=0; j<gridSizeY; j++)
            {
                Node node = nodes[i * gridSizeX + j];
                cout<<node.penalty<<"\t";
            }
            cout<<endl;
        }
        cout<<">>>>>>>>>>>>>>>>>>> walkable: "<<endl;
        for(int i=0; i<gridSizeX; i++)
        {
            for(int j=0; j<gridSizeY; j++)
            {
                Node node = nodes[i * gridSizeX + j];
                cout<<node.walkable<<"\t";
            }
            cout<<endl;
        }
    }

}
