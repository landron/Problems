
#include "IGridMaze.h"
#include "time.h"

extern bool FindCheese(IMaze* maze);

static inline 
bool TestUnit_AlreadyFound()
{
   MazeAlreadyFound maze;
   const bool found = FindCheese(&maze);
   assert(found);
   return found;
}

static inline
bool TestUnit_NoCheese()
{
   MazeNoCheese maze;
   const bool found = FindCheese(&maze);
   assert(!found);
   return !found;
}

static inline
bool TestUnit2x2_HasCheese()
{
   Maze2x2_1<true> maze1;
   bool found = FindCheese(&maze1);
   assert(found);
   assert(3 == maze1.Movements());
   if (!found)
      return false;

   Maze2x2_1<false> maze2;
   found = FindCheese(&maze2);
   assert(!found);
   // 3 * 2 (the route back)
   assert(6 == maze2.Movements());
   return found;
}

bool TestUnit2x2_NoCheese()
{
   Maze2x2_2<true> maze1;
   bool found = FindCheese(&maze1);
   assert(found);
   assert(3 == maze1.Movements() || 1 == maze1.Movements());
   if (!found)
      return false;

   Maze2x2_2<false> maze2;
   found = FindCheese(&maze2);
   assert(!found);
   // 3 * 2 (the route back); all visited
   assert(6 == maze2.Movements());
   return found;
}

void TestUnits()
{
   srand ((unsigned)time (NULL));

   (void)TestUnit_AlreadyFound();
   (void)TestUnit_NoCheese();
   (void)TestUnit2x2_HasCheese();
   (void)TestUnit2x2_NoCheese();
}