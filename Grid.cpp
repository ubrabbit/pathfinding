#include "Grid.h"
#include "Node.h"

#include <iostream>

namespace PathFind
{
    using namespace std;

    Grid::Grid(int width, int height, std::vector<std::vector<float>> tiles_costs)
    {
        gridSizeX = width;
        gridSizeY = height;

        nodes.resize(width);
        for (int i = 0; i < width; i++)
        {
            nodes[i].resize(height);
        }
        for (int x = 0; x < width; x++)
        {
            for (int y = 0; y < height; y++)
            {
                nodes[x][y] = Node(tiles_costs[x][y], x, y);
            }
        }
    }

    Grid::Grid(int width, int height, std::vector<std::vector<bool>> walkable_tiles)
    {
        gridSizeX = width;
        gridSizeY = height;

        nodes.resize(width);
        for (int i = 0; i < width; i++)
        {
            nodes[i].resize(height);
        }
        for (int x = 0; x < width; x++)
        {
            for (int y = 0; y < height; y++)
            {
                nodes[x][y] = Node(walkable_tiles[x][y], x, y);
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
        //nodes.clear();
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
                    neighbours.push_back( nodes[checkX][checkY] );
                }
            }
        }

        return neighbours;
    }

    Node Grid::GetNode(int x, int y)
    {
        return nodes[x][y];
    }

    bool Grid::SetNodeCost(int x, int y, int cost, bool walkable)
    {
        if( x >= gridSizeX ) return false;
        if( y >= gridSizeY ) return false;

        //cout<<"SetNodeCost:  "<<x<<","<<y<<"  "<<cost<<" "<<walkable<<endl;
        nodes[x][y].penalty = (float)cost;
        nodes[x][y].walkable = walkable;
        return true;
    }

    void Grid::DebugPrint()
    {
        cout<<">>>>>>>>>>>>>>>>>>> costs: "<<endl;
        for(int y=0; y<gridSizeY; y++)
        {
            for(int x=0; x<gridSizeX; x++)
            {
                Node node = nodes[x][y];
                cout<<node.penalty<<"\t";
            }
            cout<<endl;
        }
        cout<<">>>>>>>>>>>>>>>>>>> walkable: "<<endl;
        for(int y=0; y<gridSizeY; y++)
        {
            for(int x=0; x<gridSizeX; x++)
            {
                Node node = nodes[x][y];
                cout<<node.walkable<<"\t";
            }
            cout<<endl;
        }
    }

}
