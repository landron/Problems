
#include "time.h"

#include "interval_map.h"

class IntervalMapTest
{
public:
   void Run();

private:
    template<class K, class V>
    void Print(const interval_map<K,V>& vals)
    {
        typedef std::map<K,V> BaseMap;
        for (BaseMap::const_iterator it = vals.m_map.begin(); vals.m_map.end() != it; ++it)
          std::cout<<"("<<it->first<<","<<it->second<<")"<<std::endl;
        std::cout<<std::endl;
    }

   void Test1()
   {
      typedef interval_map<int, char> Interval;
      Interval vals('D');
	  vals.assign(2,5,'A');

      assert(vals[4] == 'A');
      assert(vals[1] == 'D');
      assert(vals[5] == 'D');
      assert(vals[6] == 'D');
   }

   void Test2()
   {
      typedef interval_map<unsigned, char> Interval;
      Interval vals('*');
	  vals.assign(5,6,'A');
      vals.assign(6,8,'B');
      vals.assign(9,10,'C');

      assert(vals[5] == 'A');
      assert(vals[6] == 'B');
      assert(vals[7] == 'B');
      assert(vals[9] == 'C');
      assert(vals[10] == vals[1]);
   }

   void Test3()
   {
      typedef interval_map<unsigned, char> Interval;
      Interval vals('*');
	  vals.assign(5,6,'A');
      vals.assign(6,8,'B');
      vals.assign(9,10,'C');
      assert(vals[7] == 'B');
      vals.assign(5,7,'E');

      assert(vals[5] == 'E');
      assert(vals[6] == 'E');
      assert(vals[7] == 'B');
      assert(vals[8] == '*');
   }

   void Test4()
   {
      typedef interval_map<unsigned, char> Interval;
      Interval vals('*');
	  vals.assign(5,6,'A');
      vals.assign(6,8,'B');
      vals.assign(9,10,'C');
      assert(vals[7] == 'B');
      vals.assign(5,8,'E');

      assert(vals[5] == 'E');
      assert(vals[6] == 'E');
      assert(vals[7] == 'E');
      assert(vals[8] == '*');
      assert(vals[9] == 'C');
   }

   void Test5()
   {
      typedef interval_map<unsigned, char> Interval;
      Interval vals('*');
	  vals.assign(5,6,'A');
      vals.assign(6,8,'B');
      vals.assign(11,15,'C');
      assert(vals[12] == 'C');
      assert(vals[14] == 'C');
      assert(vals.m_map.lower_bound(12)->first == 15);
      assert(vals.m_map.lower_bound(11)->first == 11);
      vals.assign(12,14,'C');   //  "extend" with the same value => nothing changes
      assert(vals.m_map.lower_bound(12)->first == 15 && "assign_2 does not pass");
      assert(vals.m_map.lower_bound(11)->first == 11);
   }

   void Test6()
   {
      typedef interval_map<unsigned, char> Interval;
      Interval vals('*');
	  vals.assign(5,6,'A');
      vals.assign(6,8,'B');
      vals.assign(11,15,'C');
      assert(vals[12] == 'C');
      assert(vals[14] == 'C');
      assert(vals.m_map.lower_bound(12)->first == 15);
      vals.assign(12,16,'C');
      assert(vals.m_map.lower_bound(15)->first == 16);
      assert(vals.m_map.lower_bound(12)->first == 16);
      assert(vals.m_map.lower_bound(11)->first == 11);
      //std::cout<<vals.m_map.lower_bound(10)->first<<std::endl;
      assert(vals.m_map.lower_bound(10)->first == 11);
      vals.assign(10,13,'C');
      assert(vals.m_map.lower_bound(11)->first == 16);
      assert(vals.m_map.lower_bound(10)->first == 10);
   }

   //   the basic test from the test itself
   void Test7_basic()
   {
      typedef interval_map<unsigned, char> Interval;
      Interval vals('A');
	  vals.assign(3,5,'B');
    
      for (size_t i = 0; i < 10 ; ++i)
      {
          switch (i)
          {
          case 3:
          case 4:
              assert(vals[i] == 'B');
          break;
          default:
              assert(vals[i] == 'A');
          break;
          }
      }
   }

   void Test8_random()
   {
      srand ((unsigned)time(NULL));

      typedef interval_map<unsigned, char> Interval;

      for (size_t i = 0; i < 1000; ++i)
      {
          if (i%25)
              std::cout<<"Test8_random no."<<(i+1)<<std::endl;

          Interval vals(0);
          const size_t noIntervals = rand() % 100 + 1;
          for (size_t i = 0; i < noIntervals; ++i)
          {
              const unsigned bottom = rand() % 100;
              const unsigned size = rand() % 10 + 1;

              const unsigned first = bottom ? vals[bottom-1] : 0;
              const unsigned last = vals[bottom+size];
              vals.assign(bottom, bottom+size, i+1);
              //std::cout<<"("<<bottom<<","<<size<<","<<i<<")"<<std::endl;
              //Print(vals);

              assert(!bottom || (first == vals[bottom-1]));
              assert(last == vals[bottom+size]);
              for (size_t j = 0; j < size; ++j)
                  assert(i+1 == vals[bottom+j]);
          }
      }
      //printf("");
   }
};

void IntervalMapTest::Run()
{
   Test1();
   Test2();
   Test3();
   Test4();
   Test5();
   Test6();
   Test7_basic();
   Test8_random();
}

void IntervalMapTest_Main()
{
   IntervalMapTest tests;
   tests.Run();
}