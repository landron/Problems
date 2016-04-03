
#include "IMaze.h"

#include <assert.h>
#include <stdexcept>
#include <utility>   // std::pair

class IGridMaze: public IMaze
{
   bool m_grid[LIMIT_MAZE][LIMIT_MAZE];   // false for wall
   const size_t m_size;
   std::pair<int, int> m_cheese;

public:
   IGridMaze(size_t size): m_size(size)
   {
      assert(size < LIMIT_MAZE);
      if (size >= LIMIT_MAZE)
         throw std::invalid_argument("The maze will be no larger than 100 by 100 units in size");

      for (int i = 0; i < LIMIT_MAZE; ++i)
         for (int j = 0; j < LIMIT_MAZE; ++j)
            m_grid[i][j] = false;  
   }

private:
   //warning C4512: 'IGridMaze' : assignment operator could not be generated
   IGridMaze(const IGridMaze&);
   IGridMaze& operator= (const IGridMaze&);
};