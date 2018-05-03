#include <vector>
#include <iostream>
#include "Node.h"
#include "Point.h"
#include "Grid.h"
#include "PathFinding.h"

using namespace std;
using namespace PathFind;

int main(){
    Point b(1,2);
    Point c(b);
    cout<<"b:   "<<b.x<<endl;
    cout<<"c:   "<<c.x<<"  "<<c.y<<endl;
    Point d = c.Set(123,456);
    cout<<"d:   "<<d.x<<"  "<<d.y<<endl;
    cout<<"b == d   "<<(b==d)<<"  "<<endl;
    cout<<"c == d   "<<(c==d)<<"  "<<endl;

    Point d2 = c.Set(-123,456);
    cout<<"d2:   "<<d2.x<<"  "<<d2.y<<endl;

    vector<bool> vect;
    for(int i=0;i<100;i++)
    {
        if (i==16 || i==25)
        {
            vect.push_back(false);
        }
        else
        {
            vect.push_back(true);
        }
    }

    Node node_1 = Node(12,0,3);
    Node node_2 = Node(node_1);
    Node node_3 = Node(12,0,3);
    cout<<"node_1 == node_2   "<<(node_1==node_2)<<"  "<<endl;
    cout<<"node_1 == node_3   "<<(node_1==node_3)<<"  "<<endl;

    Grid* g = new Grid(10,10,vect);

    for(int i=0;i<10;i++)
    {
        Pathfinding* map = new Pathfinding();
        list<Point> l= map->FindPath(*g, Point(0,0), Point(2,7));

        cout<<"point:  "<<l.size()<<endl;
        for( list<Point>::iterator iter=l.begin(); iter!=l.end(); iter++ )
        {
            cout<<" ("<<(*iter).x<<","<<(*iter).y<<") ";
        }
        cout<<endl<<"<<<<<<<<<<<<<<<<<<<<<<<<";
    }
}

