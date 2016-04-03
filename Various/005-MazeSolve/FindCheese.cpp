
//#include "stdafx.h"
#include <assert.h>
#include <utility>   // std::pair
#include <iostream>

#include "IMaze.h"

typedef std::pair<int, int> ValueType;

static inline
bool FindCheese(IMaze* maze, bool visited[2 * LIMIT_MAZE][2 * LIMIT_MAZE], ValueType& current);

void FindCheese(IMaze* maze)
{
   assert(maze);
    
   // logically, the maze should already be initialized BUT 1) as it was not precised and the function is there, plus
   //    2) the FindCheese function seems to be self sufficient 
   //    we will take the charge
   maze->Initialize();

   if (maze->Success())
      return;

   // "The maze will be no larger than 100 by 100 units" => allow 100 units in any direction   
   bool visited[2 * LIMIT_MAZE][2 * LIMIT_MAZE] = {};

   ValueType current(LIMIT_MAZE-1, LIMIT_MAZE-1);
   visited[current.first][current.second] = true;

   if (FindCheese(maze, visited, current))
      std::cout<<"Success!"<<std::endl;
}

static
bool FindCheese_Maze(IMaze* maze, bool visited[2 * LIMIT_MAZE][2 * LIMIT_MAZE], ValueType& current)
{
   ValueType::first_type& x = current.first;
   ValueType::second_type& y = current.second;

   assert(x && y);
   assert(x < 2*LIMIT_MAZE);
   assert(y < 2*LIMIT_MAZE);
   assert(!maze->Success());

   static const Direction directions[] = {left, down, right, up};
   for (int i = 0; i < sizeof(directions)/sizeof(directions[0]); ++i)
   {
      Direction d = (Direction)0;

      switch (directions[i])
      {
      case left:
         if (x > 0 && !visited[x-1][y] && maze->Move(left))
         {
            d = left;
            --x;
         }
         break;
      case up:
         if (y > 0 && !visited[x][y-1] && maze->Move(up))
         {
            d = up;
            --y;
         }
         break;
      case right:
         if (x < (2*LIMIT_MAZE-1) && !visited[x+1][y] && maze->Move(right))
         {
            d = right;
            ++x;
         }
         break;
      case down:
         if (y < (2*LIMIT_MAZE-1) && !visited[x][y+1] && maze->Move(down))
         {
            d = down;
            ++y;
         }
         break;
      }

      if (!d)
         continue;

      visited[x][y] = true;
      if (maze->Success())
         return true;
      if (FindCheese(maze, visited, current))
         return true;

      // necessary to continue ?? yes, it is a maze, not a grid
      switch (d)
      {
      case left:
         maze->Move(right);
         ++x;
         break;
      case up:
         maze->Move(down);
         ++y;
         break;
      case right:
         maze->Move(left);
         --x;
         break;
      case down:
         maze->Move(up);
         --y;
         break;
      }
   }

   assert(false && "the cheese must be out there");
   return false;
}

static
bool FindCheese_Grid(IMaze* maze, bool visited[2 * LIMIT_MAZE][2 * LIMIT_MAZE], ValueType& current)
{
   ValueType::first_type& x = current.first;
   ValueType::second_type& y = current.second;

   assert(x && y);
   assert(x < LIMIT_MAZE);
   assert(y < LIMIT_MAZE);
   assert(!maze->Success());

   if (x > 0 && !visited[x-1][y] && maze->Move(left))
   {
      x--;
   }
   else  // only one direction at time is enough
   if (y > 0 && !visited[x][y-1] && maze->Move(up))
   {
      y--;
   }
   else  // only one direction at time is enough
   if (x < LIMIT_MAZE && !visited[x+1][y] && maze->Move(right))
   {
      x++;
   }
   else  // only one direction at time is enough
   if (y < LIMIT_MAZE && !visited[x][y+1] && maze->Move(down))
   {
      y++;
   }
   else
   {
      assert(false && "the cheese must be out there");
      return false;
   }

   visited[x][y] = true;
   if (maze->Success())
      return true;
   if (FindCheese(maze, visited, current))
      return true;

   assert(false && "the cheese must be out there");
   return false;
}


// returns true if the cheese was found
bool FindCheese(IMaze* maze, bool visited[2 * LIMIT_MAZE][2 * LIMIT_MAZE], ValueType& current)
{
   return FindCheese_Maze(maze, visited, current);
}

//FindCheese_Grid
#pragma warning(disable: 4505) //Unreferenced local function has been removed
