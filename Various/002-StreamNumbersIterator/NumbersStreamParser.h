
/*
    //  Imposed interface

    class Solution {
    public:
        Solution(istream& s): m_src(s) {}
        class iterator;

        iterator begin();
        iterator end();
    }

    Allowed numbers, only one per line: spaces, +/-, any number of zeros, number, spaces
        |number| < 1000000000
*/

#include <iosfwd>
#include <string>
#include <sstream>
#include <cassert>

class Solution
{
    std::istream& m_src;
public:
    Solution(std::istream& s): m_src(s) {}
    class iterator;

    iterator begin();
    iterator end() const;

    class iterator
    {
        std::istream& m_src;
        std::streampos m_pos;
        bool m_finished;
        int m_n;

        void readNextLine(std::string&);
        bool getInteger(const std::string&, int&);

    public:
        iterator(std::istream& s, std::streampos pos, bool finished):m_src(s), m_pos(pos), m_n(0), m_finished(finished) {}

        bool operator==(const iterator& other) const {return (m_finished == other.m_finished) && (m_finished || (m_pos == other.m_pos));}
        bool operator!=(const iterator& other) const {return !operator==(other);}
        iterator& operator++();
        iterator operator++(int) {iterator tmp(*this); operator++(); return tmp;}

        int operator*() const;

    private:
        //  no assignment operator, but the generated copy constructor is necessary
        iterator& operator= (const iterator&);
    };

private:
    //  no assignment operator warnings
    Solution(const Solution&);
    Solution& operator= (const Solution&);
};

void Solution::iterator::readNextLine(std::string& line)
{
    assert(!m_src.eof());

    std::stringbuf sb;
    m_src.get(sb, 10);
    line = sb.str();

    //  skip new line
    if (!m_src.eof())
        m_src.seekg(1, std::ios_base::cur);
    m_pos = m_src.tellg();
    //  m_finished not here since we want one last read
}

bool Solution::iterator::getInteger(const std::string& line, int& n)
{
    size_t i;
    //  trim
    for (i = 0; (i < line.length()) && (' ' == line[i] || '\t' == line[i]); ++i);
    if (i == line.length())
        return false;
    // sign
    const bool negative = (line[i] == '-');
    if (negative || (line[i] == '+'))
        ++i;
    // eat zeros
    for (; (i < line.length()) && ('0' == line[i]); ++i);
    if (i == line.length())
    {
        if ((i == 0) || ('0' != line[i-1]))
            return false;
        n = 0;
        return true;
    }
    //  number
    size_t j;
    for (j = i; (j < line.length()) && ('0' <= line[j]) && ('9' >= line[j]); ++j);
    //  trim
    size_t k;
    for (k = j; (k < line.length()) && (' ' == line[k] || '\t' == line[k]); ++k);
    if (k != line.length())
        return false;

    //  too big
    if (j - i > 10)
        return false;
    if (j - i == 10)
    {
        if (line[i] != '1')
            return false;
        for (k = i+1; k < j; ++k)
            if (line[k] != '0')
                return false;
    }
    
    n = 0;
    for (k = i; k < j; ++k)
        n = n*10 + (line[k] - '0');
    if (negative)
        n = -n;

    return true;
}

Solution::iterator Solution::begin()
{
    std::streampos restore = m_src.tellg();
    m_src.seekg(0, std::ios_base::beg);
    Solution::iterator begin(m_src, m_src.tellg(), false);
    ++begin;
    m_src.seekg(restore);
    return begin;
}

Solution::iterator Solution::end() const
{
    return Solution::iterator(m_src, 0 /*it doesn't matter*/, true);
}

Solution::iterator& Solution::iterator::operator++()
{
    assert(!m_src.eof());

    //  necessary: we are using one stream only
    m_src.seekg(m_pos);

    for (m_finished = m_src.eof(); !m_finished; m_finished = m_src.eof())
    {
        std::string line;
        readNextLine(line);
        int n;
        if (getInteger(line, n))
        {
            m_n = n;
            break;
        } 
    }

    return *this;
}


int Solution::iterator::operator*() const 
{
   if (m_finished)
      throw std::overflow_error("end stream passed");
   return m_n;
}

/**
 * Example usage:
 *
 *   Solution sol(stream);
 *   for (Solution::iterator it = sol.begin(); it != sol.end(); ++it) {
 *      int x = *it;
 *      cout << x << endl;
 *   }
 */
