namespace PathFind
{
    class Point
    {
    public:
        int x;
        int y;

        Point();
        Point(int iX, int iY);
        Point(const Point& b);
        ~Point();

        int GetHashCode();

        Point Set(int iX, int iY);

        bool operator ==(const Point b);
        bool operator !=(const Point b);
    };
}
