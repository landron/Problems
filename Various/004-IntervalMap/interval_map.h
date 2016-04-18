#pragma once

//<cassert>: "In short, don't use it ; use <assert.h>."
#include <assert.h>
#include <map>
#include <limits>

#include <iostream>

template<class K, class V>
class interval_map 
{
    friend class IntervalMapTest;

public:
    typedef std::map<K,V> MapType;

private:
    MapType m_map;

public:
    // constructor associates whole range of K with val by inserting (K_min, val)
    // into the map
    interval_map( V const& val) {
        m_map.insert(m_map.begin(),std::make_pair(std::numeric_limits<K>::lowest(),val));
    };

    // The representation in m_map must be canonical, that is, consecutive map entries must not have the same value: 
   //    ..., (0,'A'), (3,'A'), ... is not allowed. 
    static bool IsCanonical(const MapType& vals)
    {
       MapType::const_iterator prev = vals.begin(), it = prev;
       ++it;
       for (; vals.end() != it && !(prev->second == it->second); prev=it, ++it);
       return (vals.end() == it);
    }
    bool IsCanonical() const
    {
       return IsCanonical(m_map);
    }

    // Assign value val to interval [keyBegin, keyEnd). 
    // Overwrite previous values in this interval. 
    // Do not change values outside this interval.
    // Conforming to the C++ Standard Library conventions, the interval 
    // includes keyBegin, but excludes keyEnd.
    // If !( keyBegin < keyEnd ), this designates an empty interval, 
    // and assign must do nothing.

    void assign( K const& keyBegin, K const& keyEnd, const V& val ) {
       assign_4(keyBegin, keyEnd, val);
       assert(IsCanonical());
    }

    //  allowing enlarging the range
    void assign_4( K const& keyBegin, K const& keyEnd, const V& val ) {
        if (!(keyBegin <  keyEnd))
            return;

        typedef std::map<K,V> BaseMap;
        typedef typename BaseMap::value_type MVT; 

        BaseMap::iterator end = m_map.upper_bound(keyEnd);
        assert((end == m_map.end() || end->first < keyEnd || keyEnd < end->first) && "equality comparison is not permitted");
        BaseMap::iterator previous(end);
        --previous;
        assert(previous != m_map.end() && "the container was already initialized");
        //  this value must be saved, before maybe being lost by the start insertion
        //     (even if might be not needed:  the end insertion might be skipped (when start != m_map.end()))
        MVT afterEnd(keyEnd, previous->second);
        
        //  do not verify against 'afterEnd' here: the interval might be enlarged downwards
        BaseMap::iterator start = m_map.lower_bound(keyBegin);
        if (start == m_map.end()) {
           previous = start;
           --previous;
           assert(previous != m_map.end());
           if (!(val == previous->second))
              start = m_map.insert(start, MVT(keyBegin, val));
        }
        else if (keyBegin < start->first) {
            --start; // needed to allow the next erase
            if (start == m_map.end() || !(val == start->second))   // not already contained
                start = m_map.insert(start, MVT(keyBegin, val));
        }
        else {
           previous = start;
           --previous;
           if ((previous == m_map.end()) || !(val == previous->second))
              start->second = val;
           else 
              start = previous;
        }

        //  insert end if needed
        //     (start value is missing when the new interval is enterily contained)
        if (start != m_map.end()) {
           assert((end == m_map.end() || end->first < keyEnd || keyEnd < end->first) && "equality comparison is not permitted (for the second comparison)");
           if (end == m_map.end() || !(keyEnd < end->first) || !(afterEnd.second == val))
               end = m_map.insert(end, afterEnd);

            //  erase old values in between
            m_map.erase(++start, end);
        }
    }


    // look-up of the value associated with key
    V const& operator[]( K const& key ) const {
        return ( --m_map.upper_bound(key) )->second;
    }

private:
   void assign_1( K const& keyBegin, K const& keyEnd, const V& val );
   void assign_2( K const& keyBegin, K const& keyEnd, const V& val );
   void assign_3( K const& keyBegin, K const& keyEnd, const V& val );
};
