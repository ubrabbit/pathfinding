#include "Point.h"

namespace PathFind
{

    Point::Point()
    {
        x = 0;
        y = 0;
    }

    Point::Point(int iX, int iY)
    {
        x = iX;
        y = iY;
    }

    Point::Point(const Point& b)
    {
        x = b.x;
        y = b.y;
    }

    Point::~Point()
    {
    }

    int Point::GetHashCode()
    {
        return x ^ y;
    }

    Point Point::Set(int iX, int iY)
    {
        if ( iX < 0 ) iX = 0;
        if ( iY < 0 ) iY = 0;

        this->x = iX;
        this->y = iY;
        return *this;
    }

    bool Point::operator ==(const Point b)
    {
        return this->x == b.x && this->y == b.y;
    }

    bool Point::operator !=(const Point b)
    {
        return !( (*this) == b );
    }

}
