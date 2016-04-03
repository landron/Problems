
enum Direction
{
    left = 1, // move left (x-1)
    down = 2, // move down (y-1)
    right = 3, // move right (x+1)
    up = 4  // move up (y+1)
};

enum
{
   LIMIT_MAZE = 100,
};

//(You don’t need to implement the maze interface below.)
struct IMaze
{
    // Will create a session and a maze.  The maze will be no larger than 100 by 100 units in size.  The mouse and a piece of cheese will be positioned at random locations within the maze.
    virtual void Initialize() = 0;
 
    // Will attempt to move the mouse in one direction.  If the move was successful, returns true.  If there was a wall and the move failed, returns false.
    virtual bool Move(Direction tryMovingMouseInThisDirection) = 0;
 
    // Will return true if the mouse and cheese are at the same location, false otherwise.
    virtual bool Success() = 0;
};
