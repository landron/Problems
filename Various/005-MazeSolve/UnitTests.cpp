
#include "IGridMaze.h"

extern bool FindCheese(IMaze* maze);

static bool TestUnit1_AlreadyFound()
{
   MazeAlreadyFound maze;
   const bool found = FindCheese(&maze);
   assert(found);
   return found;
}

void TestUnits()
{
   (void)TestUnit1_AlreadyFound();
}