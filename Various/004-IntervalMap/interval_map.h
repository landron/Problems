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

    // Assign value val to interval [keyBegin, keyEnd). 
    // Overwrite previous values in this interval. 
    // Do not change values outside this interval.
    // Conforming to the C++ Standard Library conventions, the interval 
    // includes keyBegin, but excludes keyEnd.
    // If !( keyBegin < keyEnd ), this designates an empty interval, 
    // and assign must do nothing.
    void assign( K const& keyBegin, K const& keyEnd, const V& val ) {
        // INSERT YOUR SOLUTION HERE
        assign_3(keyBegin, keyEnd, val);
    }

    void assign_1( K const& keyBegin, K const& keyEnd, const V& val ) {
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

    void assign_2( K const& keyBegin, K const& keyEnd, const V& val ) {
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

    //  protection against assigning same variable to (almost) the same interval / BUT allow enlarging the range
    void assign_3( K const& keyBegin, K const& keyEnd, const V& val ) {
        if (!(keyBegin <  keyEnd))
            return;

        typedef std::map<K,V> BaseMap;
        typedef typename BaseMap::value_type MVT; 

        BaseMap::iterator end = m_map.upper_bound(keyEnd);
        //  upper_bound can be m_map.end()
        --end;
        assert(end != m_map.end() && "the container was already initialized");
        V afterEnd(end->second);
        ++end;
        
        //  do not verify against 'afterEnd' here: the interval might be enlarged downwards
        BaseMap::iterator start = m_map.lower_bound(keyBegin);
        if (start == m_map.end())
            start = m_map.insert(start, MVT(keyBegin, val));
        else if (keyBegin < start->first)
        {
            --start;
            if (start == m_map.end() || (val != start->second))
                start = m_map.insert(start, MVT(keyBegin, val));
        }
        else
            start->second = val;

        //  insert end if needed
        if (end == m_map.end() || (keyEnd > end->first) || (afterEnd != val))
            end = m_map.insert(end, MVT(keyEnd, afterEnd));

        //  erase old values in between
        if (start != m_map.end())
            m_map.erase(++start, end);
    }


    // look-up of the value associated with key
    V const& operator[]( K const& key ) const {
        return ( --m_map.upper_bound(key) )->second;
    }
};
