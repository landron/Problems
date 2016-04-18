
#include "IGridMaze.h"

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
   return found;
}

void TestUnits()
{
   (void)TestUnit_AlreadyFound();
   (void)TestUnit_NoCheese();
}