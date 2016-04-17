
#include "time.h"

#include "interval_map.h"
#include "interval_map_extra.h"

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

   void Test0_Limit()
   {
      typedef interval_map<int, char> Interval;
      Interval vals('D');

      vals.assign(2,2,'A');
      for (int i = -1; i < 4; ++i)
         assert(vals[i] == 'D');
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

      //std::cout<<(--vals.m_map.lower_bound(12))->first<<std::endl;
      assert((--vals.m_map.lower_bound(12))->first == 10);
      assert(vals.m_map.lower_bound(12) == vals.m_map.end());

      for (int  i = 0; i < 15; ++i)
         assert(vals[i] != 'A');
      for (int  i = 10; i < 15; ++i)
         assert(vals[i] == '*');
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

   //   the basic test from the problem itself
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

#ifdef _DEBUG
   void Test8_random()
   {
      srand ((unsigned)time(NULL));

      typedef interval_map<unsigned, char> Interval;
      typedef Interval::MapType::value_type::second_type ValueType;

      for (size_t i = 0; i < 1000; ++i)
      {
         if (0 == (i+1)%25)
            std::cout<<"Test8_random no."<<(i+1)<<std::endl;

         Interval vals(0);
         const ValueType noIntervals = rand() % 100 + 1;
         for (ValueType i = 0; i < noIntervals; ++i)
         {
            const unsigned bottom = rand() % 100;
            const unsigned size = rand() % 10 + 1;

            const ValueType first = bottom ? vals[bottom-1] : 0;
            const ValueType last = vals[bottom+size];
            vals.assign(bottom, bottom+size, i+1);
            //std::cout<<"("<<bottom<<","<<size<<","<<i<<")"<<std::endl;
            //Print(vals);

            assert(!bottom || (first == vals[bottom-1]));
            assert(last == vals[bottom+size]);
            for (size_t j = 0; j < size; ++j)
               assert(i+1 == vals[bottom+j]);
         }
      }
      std::cout<<std::endl;
   }
#endif //_DEBUG

   // not covered by assign_3
   void Test9_validate_canonical() 
   {
      typedef interval_map<unsigned, char> Interval;
      Interval vals('A');
      vals.assign(3,5,'A');
      assert(vals.m_map.size() == 1);
      assert(vals[1] == 'A');

      vals.assign(3,8,'B');
      assert(vals.m_map.size() == 3);
      vals.assign(2,7,'B');
      assert(vals.m_map.size() == 3);
      assert(vals[8] == 'A');

      vals.assign(5,10,'B');
      assert(vals.m_map.size() == 3);
      assert(vals[1] == 'A');
      assert(vals[2] == 'B');
      assert(vals[9] == 'B');
      assert(vals[10] == 'A');
      vals.assign(2,6,'A');
      assert(vals.m_map.size() == 3);
      assert(vals[5] == 'A');
      assert(vals[6] == 'B');
      assert(vals[6] == 'B');

      //Print(vals);
   }

   void Test10_validate_canonical() 
   {
      typedef interval_map<unsigned, char> Interval;
      Interval vals('A');
      vals.assign(3,5,'B');
      vals.assign(3,7,'B');
      assert(vals.m_map.size() == 3);
      assert(vals[6] == 'B');
      assert(vals[7] == 'A');
      vals.assign(5,9,'B');
      assert(vals.m_map.size() == 3);
      assert(vals[8] == 'B');
      assert(vals[9] == 'A');
   }
};

void IntervalMapTest::Run()
{
   Test0_Limit();

   Test1();
   Test2();
   Test3();
   Test4();
   Test5();
   Test6();
   Test7_basic();
   Test9_validate_canonical();
   Test10_validate_canonical();

#ifdef _DEBUG
#if 0
   Test8_random();
#endif
#endif //_DEBUG
}

void IntervalMapTest_Main()
{
   IntervalMapTest tests;
   tests.Run();
}