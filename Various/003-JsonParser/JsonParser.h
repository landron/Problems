
//  TODO
/*
   1.  try to const as much as possible
   2.  think of a version that works directly with istream
         for fun, as string is not very expensive since JSON is thought for not very large tansfers (I think)
*/

#pragma once

#include <iostream>

enum
{
   TYPE_UNDEFINED,
   TYPE_INPUT,
   TYPE_MALFORMED,
   TYPE_EMPTY,     //  nothing, empty object
   TYPE_NULL,
   TYPE_STRING,
   TYPE_BOOL,
   TYPE_ARRAY,
   TYPE_OBJECT,    //  dictionary
};

// TODO
template<unsigned T, class U>
struct JsonValue
{ 
   typedef U type;

   unsigned Type() const {return T;}
};
template <> 
struct JsonValue<TYPE_STRING, std::string>
{};
typedef struct JsonValue<TYPE_STRING, std::string> JsonValueString;
//template <> 
//struct JsonValue<TYPE_UNDEFINED, int>
//{};

class JsonItem
{
   const std::wstring m_src;
   const unsigned m_type;

public:
   JsonItem(const std::wstring& item, unsigned type): m_src(item), m_type(type) {}

   class iterator
   {
      const std::wstring m_src;
      size_t m_pos;

   public:
      explicit iterator(const std::wstring& src): m_src(src), m_pos(0) {}

      bool operator==(const iterator& other) const {return (m_src.length() == m_pos) == (other.m_src.length() == other.m_pos);}
      bool operator!=(const iterator& other) const {return !operator==(other);}

      iterator& operator++();
      iterator operator++(int) {iterator tmp(*this); operator++(); return tmp;}

      unsigned Type() const {/*TODO*/return TYPE_UNDEFINED;};
      //template<unsigned T, class U>
      //JsonValue<T,U> operator*() const;
      JsonItem operator*() const;

   private:
      iterator& operator= (const iterator&);
   };

   iterator begin() {/*TODO*/return iterator(L"");}
   iterator end() {/*TODO*/return iterator(L"");}

   unsigned Type() const {return m_type;}
   std::wstring Name() const;
   //   TODO: Value

private:
   // the generated one is good
   //JsonItem(const JsonItem& other)
   // cannot be made as the string is const
   JsonItem& operator= (const JsonItem& other);
};

class JsonParser
{
   std::wistream& m_src;

public:
   JsonParser(std::wistream& src): m_src(src) {}

   JsonItem::iterator begin();
   JsonItem::iterator end();

private:
   JsonParser(const JsonParser&);
   JsonParser& operator= (const JsonParser&);
};