#pragma once

#include "interval_map.h"

template<class K, class V>
void interval_map<K,V>::assign_1( K const& keyBegin, K const& keyEnd, const V& val ) {
   if (!(keyBegin <  keyEnd))
      return;

   std::pair<bool, V> afterEnd;
   afterEnd.first = false;
   typedef std::map<K,V> BaseMap;
   BaseMap::iterator end = m_map.upper_bound(keyEnd);
   --end;
   assert((m_map.end() != end) && "there must be a value");
   if (m_map.end() != end)
      afterEnd.second = end->second;
   ++end;

   BaseMap::iterator start = m_map.lower_bound(keyBegin);
   if (start == m_map.end() || (keyBegin != start->first))
   {
      typedef typename BaseMap::value_type MVT; 
      start = m_map.insert(start, MVT(keyBegin, val));
   }

   if (end == m_map.end())
   {
      typedef typename BaseMap::value_type MVT;
      end = m_map.insert(end, MVT(keyEnd, afterEnd.second));
   }
}

template<class K, class V>
void interval_map<K,V>::assign_2( K const& keyBegin, K const& keyEnd, const V& val ) {
   if (!(keyBegin <  keyEnd))
      return;

   typedef std::map<K,V> BaseMap;
   BaseMap::iterator end = m_map.upper_bound(keyEnd);
   --end;
   V afterEnd(end->second);
   ++end;

        
   BaseMap::iterator start = m_map.lower_bound(keyBegin);
   if (start == m_map.end() || (keyBegin != start->first))
   {
      typedef typename BaseMap::value_type MVT; 
      start = m_map.insert(start, MVT(keyBegin, val));
   }
   else
      start->second = val;

   //  insert end if needed
   if (end == m_map.end() || (keyEnd != end->first))
   {
      typedef typename BaseMap::value_type MVT;
      end = m_map.insert(end, MVT(keyEnd, afterEnd));
   }

   //  erase old values in between
   m_map.erase(++start, end);
}
