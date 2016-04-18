
#include "IMaze.h"

#include <assert.h>
#include <stdexcept>
#include <utility>   // std::pair

class IGridMaze: public IMaze
{
protected:
   bool m_grid[LIMIT_MAZE][LIMIT_MAZE];   // false for wall
   const size_t m_size;
   std::pair<unsigned, unsigned> m_cheese;
   std::pair<unsigned, unsigned> m_mouse;

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


   virtual bool Success() const
   {
      return m_cheese == m_mouse;
   }

private:
   //warning C4512: 'IGridMaze' : assignment operator could not be generated
   IGridMaze(const IGridMaze&);
   IGridMaze& operator= (const IGridMaze&);
};

class MazeAlreadyFound: public IGridMaze
{
   typedef IGridMaze ParentClass;

public:
   MazeAlreadyFound(): ParentClass(1) {}

   virtual void Initialize()
   {
      assert(!m_cheese.first && !m_cheese.first);
      assert(!m_mouse.first && !m_mouse.first);
   }

   virtual bool Move(Direction)
   {
      return false;
   }
};
