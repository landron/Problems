/* 
   http://www.hackerrank.com/challenges/bitset-1
   tag_floyd, tag_cycle
*/

#include <assert.h>
#include <cstdint>
#include <iostream>
using namespace std;

uint32_t get_distinct_by_prev_validation(uint32_t N, uint32_t S, uint32_t P, uint32_t Q)
{
   uint32_t length = 0;
   for (uint32_t curr = S, prev = curr-1; prev != curr && length < N; prev = curr, curr = P*curr+Q, ++length);
   return length;
}

uint32_t get_distinct_by_Floyd(uint32_t N, uint32_t S, uint32_t P, uint32_t Q, bool print=false)
{
   uint32_t turtle(P*S+Q);
   uint32_t hare(P*turtle+Q);

   for (unsigned i = 0; turtle != hare && (i < N); ++i)
   {
      turtle = P*turtle+Q;
      hare = P*(P*hare+Q)+Q;
   }
   if (turtle != hare)
      return N;

   // reset turtle
   turtle = S;
   auto first_repetition = 0;
   for (; turtle != hare; ++first_repetition)
   {
      if (print)
         cout<<hex<<turtle<<endl;
      turtle = P*turtle+Q;
      hare = P*hare+Q;
   }
   if (print)
      cout<<hex<<turtle<<endl;

   auto length_cycle = 1;
   for (hare = P*turtle+Q; turtle != hare; ++length_cycle)
   {
      if (print)
         cout<<hex<<hare<<endl;
      hare = P*hare+Q;
   }
   if (print)
      cout<<hex<<hare<<endl;

   return (first_repetition+1)+(length_cycle-1);
}

int get_distinct(uint32_t N, uint32_t S, uint32_t P, uint32_t Q)
{
   return get_distinct_by_Floyd(N, S, P, Q);
}

void read_and_solve()
{
   uint32_t N, S, P, Q;
   cin >> N >> S >> P >> Q;

   auto distinct = get_distinct(N, S, P, Q);
   if (distinct != N)
      // problem error ? cycle length instead of distinct numbers
         cout << dec << distinct-1;
   else
      cout << dec << distinct;
}

void debug_validations()
{
   assert(2 == get_distinct(32, 2, 2147483647, 2));
   assert(4 == get_distinct(100000000, 1, 1024, 9));
   assert(32 == get_distinct(100000000, 569099406, 1607140150, 823906344));
   assert(27 == get_distinct(100000000, 1232077670, 126810854, 1536183938));
   assert(10000000 == get_distinct(10000000, 658061970, 695098531, 1430548937));

   // good anwsers
   assert(4 == get_distinct_by_prev_validation(1000, 1, 1024, 9));
   assert(32 == get_distinct_by_prev_validation(100000000, 569099406, 1607140150, 823906344));
   assert(27 == get_distinct_by_prev_validation(100000000, 1232077670, 126810854, 1536183938));
   assert(10000000 == get_distinct_by_prev_validation(10000000, 658061970, 695098531, 1430548937));
   // bad answers
   assert(1000 == get_distinct_by_prev_validation(1000, 2, 2147483647, 2));
}

int main() 
{
   debug_validations();
   //read_and_solve();

   return 0;
}