
#include "IMaze.h"

#include <assert.h>
#include <stdexcept>
#include <utility>   // std::pair

/*
   x is the first coordinate, left to right; y is the second, from bottom to above
*/
class IGridMaze: public IMaze
{
   bool m_grid[LIMIT_MAZE][LIMIT_MAZE];   // false for wall
   const size_t m_size;
   std::pair<unsigned, unsigned> m_cheese;
   std::pair<unsigned, unsigned> m_mouse;

   unsigned m_movements;

public:
   IGridMaze(size_t size): m_size(size), m_movements(0)
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

   virtual bool Move(Direction d)
   {
      const bool allowed = Allowed(d);
      if (!allowed)
         return false;

      const std::pair<unsigned, unsigned> initial(m_mouse);
      ReallyMove(d);
      assert(m_mouse != initial);
      return true;
   }

   unsigned Movements() const {return m_movements;}

protected:
   const std::pair<unsigned, unsigned>& Mouse() const {return m_mouse;}
   bool MouseIs(unsigned x, unsigned y) const {return x == m_mouse.first && y == m_mouse.second;}

   const std::pair<unsigned, unsigned>& Cheese() const {return m_cheese;}
   void SetCheese(unsigned x, unsigned y) 
   {
      assert(x < m_size && y < m_size);
      m_cheese.first = x;
      m_cheese.second = y;
   }
   void SetNoCheese() 
   {
      m_cheese.first = 2*m_size+1;
   }

private:
   // TODO: validate consistency = if right is possible, then left is possible also for the opposite point
   virtual bool Allowed(Direction) const = 0;

   void ReallyMove(Direction d)
   {
      switch (d)
      {
      case left: 
         {
            assert(m_mouse.first);
            --m_mouse.first;
         }
         break;
      case up: 
         {
            assert(m_mouse.second < m_size);
            ++m_mouse.second;
         }
         break;
      case down: 
         {
            assert(m_mouse.second);
            --m_mouse.second;
         }
         break;
      case right: 
         {
            assert(m_mouse.first < m_size);
            ++m_mouse.first;
         }
         break;

      default:
         assert(false);
      };

      ++m_movements;
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
      assert(!Cheese().first && !Cheese().second);
      assert(!Mouse().first && !Mouse().second);
   }

   virtual bool Allowed(Direction) const
   {
      return false;
   }
};

class MazeNoCheese: public IGridMaze
{
   typedef IGridMaze ParentClass;

public:
   MazeNoCheese(): ParentClass(1) {}

   virtual void Initialize()
   {
      assert(!Mouse().first && !Mouse().second);
      SetNoCheese();
   }

   virtual bool Allowed(Direction) const
   {
      return false;
   }
};

enum
{
   TYPE_CHEESE_NO_CHEESE = 1,
   TYPE_CHEESE_HAS_CHEESE,
   TYPE_CHEESE_RANDOM_CHEESE
};

// one route possible: up, right, down
template <unsigned _cheese>
class Maze2x2_1: public IGridMaze
{
   typedef IGridMaze ParentClass;

public:
   Maze2x2_1(): ParentClass(2) {}

   virtual void Initialize();

   virtual bool Allowed(Direction d) const
   {
      switch (d)
      {
      case left:  return MouseIs(1,1);
      case right: return MouseIs(0,1);
      case up:    return 0 == Mouse().second;
      case down:  return 1 == Mouse().second;
      };

      assert(false);
      return false;
   }
};

template <>
virtual void Maze2x2_1<TYPE_CHEESE_RANDOM_CHEESE>::Initialize()
{
   SetCheese(1, 0);
}

template <>
virtual void Maze2x2_1<TYPE_CHEESE_HAS_CHEESE>::Initialize()
{
   SetCheese(1, 0);
}

template <>
virtual void Maze2x2_1<TYPE_CHEESE_NO_CHEESE>::Initialize()
{
   SetNoCheese();
}

// two routes possible: up, right, down + right
template <unsigned _cheese>
class Maze2x2_2: public Maze2x2_1<_hasCheese>
{
   typedef Maze2x2_1<_hasCheese> ParentClass;

public:
   virtual bool Allowed(Direction d) const
   {
      switch (d)
      {
         case left:  return 1 == Mouse().first;
         case right: return 0 == Mouse().first;
      }
      return ParentClass::Allowed(d);
   }
};
