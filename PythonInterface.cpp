#include "PythonInterface.h"
#include "PathFinding.h"
#include "Grid.h"
#include "Point.h"

#include <iostream>

namespace PathFind
{

    using namespace std;

    extern "C"
    {
        #include <time.h>
        #ifndef PYTHON_PATH
            #ifdef _WIN32
                #define PYTHON_PATH <Python.h>
            #else
                #define PYTHON_PATH "python3.5/Python.h"
            #endif
            #include PYTHON_PATH
        #endif

        static Grid* g_Map = nullptr;
        #ifndef INIT_MAP
            #define INIT_MAP { if(g_Map!=nullptr){ delete g_Map; g_Map=nullptr; } }
        #endif

        static PyObject* CreateMapByCost(PyObject *self, PyObject *args)
        {
            INIT_MAP;

            long width, height;
            PyObject *posList, *tmpPos;
            PyArg_ParseTuple(args,"llO",&width, &height, &posList);

            cout<<"CreateMapByCost: "<<width<<"  "<<height<<endl;
            int size_pos = PyList_Size(posList);
            assert( (width*height == size_pos) );

            vector<float> tiles_costs;
            for(int i=0; i<size_pos; i++)
            {
                tiles_costs.push_back(0);
            }
            for(int i=0; i<size_pos; i++)
            {
                tmpPos = PyList_GetItem(posList, i);
                int pos_x = PyLong_AsLong(PyTuple_GetItem(tmpPos,0));
                int pos_y = PyLong_AsLong(PyTuple_GetItem(tmpPos,1));
                long cost = PyLong_AsLong(PyTuple_GetItem(tmpPos,2));
                tiles_costs[ pos_x*width + pos_y ] = (float)cost;
            }
            Grid* grid = new Grid(width, height, tiles_costs);
            g_Map = grid;

            grid->DebugPrint();
            return Py_BuildValue("i",1);
        }

        static PyObject* CreateMapByBlock(PyObject *self, PyObject *args)
        {
            INIT_MAP;

            long width, height;
            PyObject *blockList, *tmpPos;
            PyArg_ParseTuple(args,"llO",&width, &height, &blockList);

            cout<<"CreateMapByBlock: "<<width<<"  "<<height<<endl;
            int size_pos = PyList_Size(blockList);

            vector<bool> tiles_walkable;
            for(int i=0; i<size_pos; i++)
            {
                tiles_walkable.push_back( true );
            }
            for(int i=0; i<size_pos; i++)
            {
                tmpPos = PyList_GetItem(blockList, i);
                int pos_x = PyLong_AsLong(PyTuple_GetItem(tmpPos,0));
                int pos_y = PyLong_AsLong(PyTuple_GetItem(tmpPos,1));
                tiles_walkable[ pos_x*width + pos_y ] = false;
            }
            Grid* grid = new Grid(width, height, tiles_walkable);
            g_Map = grid;

            grid->DebugPrint();
            return Py_BuildValue("i",1);
        }

        static PyObject* CreateMap(PyObject *self, PyObject *args)
        {
            INIT_MAP;

            long width, height;
            PyObject *posList, *blockList, *tmpPos;
            PyArg_ParseTuple(args,"llOO",&width, &height, &posList, &blockList);

            cout<<"create Map: "<<width<<"  "<<height<<endl;
            int size_pos = PyList_Size(posList);
            assert( (width*height == size_pos) );

            vector<float> tiles_costs;
            for(int i=0; i<size_pos; i++)
            {
                tiles_costs.push_back(0);
            }
            for(int i=0; i<size_pos; i++)
            {
                tmpPos = PyList_GetItem(posList, i);
                int pos_x = PyLong_AsLong(PyTuple_GetItem(tmpPos,0));
                int pos_y = PyLong_AsLong(PyTuple_GetItem(tmpPos,1));
                long cost = PyLong_AsLong(PyTuple_GetItem(tmpPos,2));
                tiles_costs[ pos_x*width + pos_y ] = (float)cost;
            }
            Grid* grid = new Grid(width, height, tiles_costs);

            int size_block = PyList_Size(blockList);
            for(int i=0; i<size_block; i++)
            {
                tmpPos = PyList_GetItem(blockList,i);
                int pos_x = PyLong_AsLong(PyTuple_GetItem(tmpPos,0));
                int pos_y = PyLong_AsLong(PyTuple_GetItem(tmpPos,1));
                grid->SetNodeCost( pos_x, pos_y, 0xFFFF, false );
            }

            g_Map = grid;
            grid->DebugPrint();
            return Py_BuildValue("i",1);
        }

        static PyObject* DeleteMap(PyObject *self, PyObject *args)
        {
            INIT_MAP;
            return Py_BuildValue("i",1);
        }

        static PyObject* SetGridCost(PyObject *self, PyObject *args)
        {
            if(g_Map==nullptr)
            {
                return Py_BuildValue("i", -1);
            }

            PyObject *tmpPos, *posList;

            PyArg_ParseTuple(args,"O", &posList);
            int len = PyList_Size(posList);

            for(int i=0; i<len; i++)
            {
                long pos_x, pos_y, cost, able;
                bool walkable;
                tmpPos = PyTuple_GetItem(posList,i);
                pos_x = PyLong_AsLong(PyTuple_GetItem(tmpPos,0));
                pos_y = PyLong_AsLong(PyTuple_GetItem(tmpPos,1));
                cost = PyLong_AsLong(PyTuple_GetItem(tmpPos,2));
                able = PyLong_AsLong(PyTuple_GetItem(tmpPos,3));
                walkable = true ? (able!=0) : false;

                g_Map->SetNodeCost( pos_x, pos_y, cost, walkable );
            }
            return Py_BuildValue("i", 1);
        }

        static PyObject* SeekPath(PyObject *self, PyObject *args)
        {
            assert( g_Map != nullptr );

            long enter_x, enter_y, exit_x, exit_y;
            PyObject *oEnter,*oExit;

            PyArg_ParseTuple(args,"OO", &oEnter, &oExit);

            enter_x=PyLong_AsLong(PyTuple_GetItem(oEnter,0));
            enter_y=PyLong_AsLong(PyTuple_GetItem(oEnter,1));
            exit_x=PyLong_AsLong(PyTuple_GetItem(oExit,0));
            exit_y=PyLong_AsLong(PyTuple_GetItem(oExit,1));

            clock_t startTime,endTime;
            long cost = 0;

            list<Point> ret;
            Point pointStart = Point(enter_x, enter_y);
            Point pointEnd = Point(exit_x, exit_y);

            startTime = clock();
            Pathfinding pathFind = Pathfinding();
            ret = pathFind.FindPath(*g_Map, pointStart, pointEnd);
            endTime = clock();
            cost = (long)(((endTime - startTime)*1000.0) / CLOCKS_PER_SEC);

            PyObject *tuple_return, *tuple_param;
            tuple_return = PyTuple_New(2);
            tuple_param = PyTuple_New(ret.size()*2);
            PyTuple_SetItem(tuple_return,0,Py_BuildValue("i",cost));
            int i=0;
            for( list<Point>::iterator iter=ret.begin(); iter!=ret.end(); iter++ )
            {
                Point tmpP = *iter;
                PyTuple_SetItem(tuple_param,i++,Py_BuildValue("i",tmpP.x));
                PyTuple_SetItem(tuple_param,i++,Py_BuildValue("i",tmpP.y));
            }
            PyTuple_SetItem(tuple_return,1,tuple_param);
            return tuple_return;
        }

        static PyObject* SeekPathDebug(PyObject *self, PyObject *args)
        {
            long execute_cnt;
            PyObject *SeekArgs;
            PyArg_ParseTuple(args,"lO", &execute_cnt, &SeekArgs);

            clock_t startTime,endTime;
            long cost = 0;
            PyObject *tuple_return;
            startTime = clock();
            for(int i=0; i<execute_cnt-1; i++)
            {
                SeekPath(self, SeekArgs);
            }
            tuple_return = SeekPath(self, SeekArgs);
            endTime = clock();
            cost = (long)(((endTime - startTime)*1000.0) / CLOCKS_PER_SEC);
            PyTuple_SetItem(tuple_return, 0, Py_BuildValue("l",cost));
            return tuple_return;
        }

        static PyMethodDef PathMethods[] = {
                {"CreateMap", CreateMap, METH_VARARGS, "CreateMap"},
                {"CreateMapByCost", CreateMapByCost, METH_VARARGS, "CreateMapByCost"},
                {"CreateMapByBlock", CreateMapByBlock, METH_VARARGS, "CreateMapByBlock"},
                {"DeleteMap", DeleteMap, METH_VARARGS, "DeleteMap"},
                {"SetGridCost", SetGridCost, METH_VARARGS, "SetGridCost"},
                {"SeekPath", SeekPath, METH_VARARGS, "SeekPath"},
                {"SeekPathDebug", SeekPathDebug, METH_VARARGS, "SeekPathDebug"},
                {NULL,NULL,0,NULL},
        };

        static struct PyModuleDef PathModule = {
                PyModuleDef_HEAD_INIT,
                "c_path",
                "c_path",
                -1,
                PathMethods,
        };

        PyMODINIT_FUNC PyInit_c_path(void){
                return PyModule_Create(&PathModule);
        }

    }
}
