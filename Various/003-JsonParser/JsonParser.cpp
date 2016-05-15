// tag_parser

// TODO
/*
   1. a better implementation, usign some regex
        http://boost-spirit.com/
*/

/*
   Knowledge base
   1. format http://www.json.org/ , http://en.wikipedia.org/wiki/JSON

   2. limit cases
         "Unfortunately the JSON specification does not allow a trailing comma."
*/

#include <cassert>
#include <iostream>
#include <limits>

#include "JsonParser.h"

struct JValue
{
   int type;
   size_t start;
   size_t size;

   JValue(): type(TYPE_UNDEFINED), start(0), size(0) {}
};

struct JResult
{
   bool result;
   size_t next;

   JResult(): result(false), next(0) {}
};

static JResult GetArray(const wchar_t*, size_t, JValue&);
static JResult GetObject(const wchar_t*, size_t, JValue&);

static inline
bool Trim(wchar_t c)
{
   switch (c)
   {
   case L' ':
   case L'\t':
   case L'\r':
   case L'\n':
      return true;
   default:
      return false;
   };
}

static 
size_t Trim(const wchar_t* src, size_t len)
{
   assert(src && len);
   size_t i;
   for (i = 0; (i < len) && Trim(src[i]); ++i);
   return i;
}

//  the positions must be updated outside
static inline
bool GetString(const wchar_t* src, size_t len, JValue& value)
{
   assert(src && len);
   assert(L'"' == *src);
   size_t i;
   for (i = 1; i < len; ++i)
   {
      if (L'"' == src[i] && ((i ==0) || (L'\\' != src[i-1])))
         break;
   }
   if (i == len)
      return false;

   value.type = TYPE_STRING;
   value.start = 1;
   assert(i);
   value.size = i-1;

   //  tag_trace
   if (0)
   {
      std::wstring trace(src, 1, i-1);
      wprintf(L"GetString: \"%s\"\n", trace.c_str());
   }

   return true;
}

static
JResult GetValue(const wchar_t* src, size_t len, JValue& value)
{
   JResult result;
   size_t& next = result.next;

   next = Trim(src, len);
   assert(next <= len);
   if (next == len)
      return result;

   switch (src[next])
   {
   case L'"':
      {
         if (!GetString(src+next, len-next, value))
            return result;
         assert(value.type == TYPE_STRING);
         assert(value.start == 1);
         assert(value.size <= len-next);

         //  update positions
         value.start += next;

         next += (1+value.size+1); //  skip two '"'
         result.result = true;

         return result;
      }
      break;

   case L'[':
      {
         size_t offset = next;
         JResult result = GetArray(src+next, len-next, value);
         value.size += offset;
         result.next += offset;
         return result;
      }
      break;

   case L'{':
      {
         size_t offset = next;
         JResult result =  GetObject(src+next, len-next, value);
         value.size += offset;
         result.next += offset;
         return result;
      }
      break;

   case L't':
   case L'f':
   case L'n':
      {
         if (0 == wcsncmp(src+next, L"true", 4) || 0 == wcsncmp(src+next, L"null", 4) )
         {
            value.type = (src[next] == L't') ? TYPE_BOOL : TYPE_NULL;
            value.start = next;
            value.size = 4;

            next += 4;
            result.result = true;
         }
         else if (0 == wcsncmp(src+next, L"false", 5))
         {
            value.type = TYPE_BOOL;
            value.start = next;
            value.size = 5;

            next += 5;
            result.result = true;
         }

         return result;
      }
      break;

   default:
      assert(!result.result);
      //  do not know how to treat it
      return result;
   }
}

JResult GetArray(const wchar_t* src, size_t len, JValue& theArray)
{
   JResult result;
   size_t& next = result.next;

   assert(src && len);
   assert(L'[' == *src);
   if (1 == len)
      return result;

   bool foundValue = false;
   for (next = 1; next < len;)
   {
      size_t i = next;
      JValue value;
      JResult temp = GetValue(src+i, len-i, value);
      next = temp.next + i;
      assert(next <= len);
      //  ']' if not value found (empty array) 
      if (!temp.result)
      {   
         if ((next < len) && (L']' == src[next]) && !foundValue)
            break;
         return result;
      }
      foundValue = true;

      i = next;
      next = Trim(src+i, len-i);
      if (next == len-i)
         return result;
      next += i;
      assert(next < len);
      if (L']' == src[next])
         break;
      if (L',' != src[next])
         return result;

      i = next+1;
      next = Trim(src+i, len-i);
      if (next == len-i)
         return result;
      next += i;
      assert(next < len);
   }

   assert(L']' == src[next]);
   ++next;

   theArray.type = TYPE_ARRAY;
   theArray.start = 0;
   theArray.size = next;

   result.result = true;
   return result;
}

JResult Object_GetNextItem(const wchar_t* src, size_t len, const size_t fromPos, 
                           JValue& name, JValue& value, bool& end)
{
   JResult result;
   size_t& next = result.next;

   assert(src && len);
   if ((0 == fromPos) && (L'{' == *src))
   {
      if (1 == len)
         return result;
      next = 1;
   }
   else
      next = fromPos;

   size_t i = next;
   next = Trim(src+i, len-i);
   if (next == len-i)
      return result;
   next += i;
   assert(next < len);

   //JValue name;
   if (  L'"' != src[next] ||    // invalid JSON
         !GetString(src+next, len-next, name))
   {
      //  empty object accepted
      if ((next < len) && (L'}' == src[next]) && (0 == fromPos))
      {
         name.type = TYPE_EMPTY;
         value.type = TYPE_EMPTY;
         result.result = true;
      }
      return result;
   }
   name.start += next;
   next += (1+name.size+1);   //  skip 2 '"'

   i = next;
   next = Trim(src+i, len-i);
   if (next == len-i)
      return result;
   next += i;
   assert(next < len);
   if (L':' != src[next])
      return result;

   i = next+1;
   //JValue value;
   JResult temp = GetValue(src+i, len-i, value);
   next = temp.next + i;
   if (!temp.result || (next == len))
      return result;
   assert(next < len);
   value.start += i;

   i = next;
   next = Trim(src+i, len-i);
   if (next == len-i)
      return result;
   next += i;
   assert(next < len);
   //printf("%c\n", src[next]);
   if (L'}' != src[next])
   {
      if (L',' != src[next])
         return result;
   }
   else
      end = true;
   ++next;

   if (len != next)
   {
      i = next;
      next = Trim(src+i, len-i);
      if (next == len-i)
         return result; // abrupt ending
      next += i;
   }
   assert(next <= len);

   result.result = true;
   return result;
}

JResult Object_GetNextItem(const wchar_t* src, size_t len, const size_t fromPos, 
                           std::wstring& nameOut, JValue& valueOut, bool& end)
{
   JValue name, value;
   JResult result = Object_GetNextItem(src, len, fromPos, name, value, end);
   if (result.result)
   {
      nameOut = std::wstring(src, name.start, name.size);
      valueOut = value;
   }
   return result;
}

// ignore (ending) parsing error as we alreay checked them previously AND we are only interested in the values
void Object_GetNextItem_IgnoreParseErrors(const wchar_t* src, size_t len, const size_t fromPos, 
                                             std::wstring& nameOut, JValue& valueOut)
{
   bool end;
   JValue name, value;
   JResult result = Object_GetNextItem(src, len, fromPos, name, value, end);
   
   nameOut = std::wstring(src, name.start, name.size);
   valueOut = value;
}

//  fromPos = 0 => all object, otherwise the first next one
JResult GetObject(const wchar_t* src, size_t len, JValue& object)
{
   JResult result;
   size_t& next = result.next;

   bool end = false;
   for (next = 0; (next < len) && !end; )
   {
      std::wstring name;
      JValue value;
      result = Object_GetNextItem(src, len, next, name, value, end);
      if (!result.result)
         return result;

      //  tag_trace
      if (0)
      {
         wprintf(L"Object_GetNextItem: \"%s\"\n", name.c_str());
      }
   }

   object.type = TYPE_OBJECT;
   object.start = 1;
   object.size = next;

   return result;
}

static 
bool GetJSON(std::wistream& src, std::wstring& jsonOut)
{
   src.seekg(0, std::ios_base::beg);

   src.ignore(std::numeric_limits<std::streamsize>::max(), L'{');
   if (!src)
      return false;
   src.seekg(-1, std::ios_base::cur);
   const std::wistream::pos_type start = src.tellg();
   src.seekg(1, std::ios_base::cur);

   int balance = 1;
   while (balance != 0)
   {
      assert(balance > 0);

      wchar_t buff[256];
      src.get(buff, sizeof(buff)/sizeof(wchar_t), L'}');
      for (int i = 0; buff[i] != L'\0'; ++i)
      {
         assert(i < src.gcount());

         switch (buff[i])
         {
         case L'}':
            if (balance == 0)
               return false;
            --balance;
            break;
         case L'{':
            ++balance;
            break;
         };
      }
      if (!src)
         return false;

      src.seekg(1, std::ios_base::cur);
      if (balance == 0)
         return false;
      --balance;
   }

   const std::wistream::pos_type stop = src.tellg();
   jsonOut.clear();
   jsonOut.reserve(stop-start+1);

   src.seekg(start, std::ios_base::beg);
   wchar_t buff[256];
   for (int i = stop-start; i > 0; i -= (sizeof(buff)/sizeof(wchar_t)-1))
   {
      src.read(buff, std::min<int>(i, sizeof(buff)/sizeof(wchar_t)-1));
      buff[src.gcount()] = L'\0';

      jsonOut += buff;
   }

   return true;
}


JsonItem::iterator JsonParser::begin()
{
   std::wstring json;
   if (!GetJSON(m_src, json))
      return end();

   //  validate
   JValue object;
   JResult validate = GetObject(json.c_str(), json.length(), object);
   if (!validate.result)
      return end();

   return JsonItem::iterator(json);
}

JsonItem::iterator JsonParser::end()
{
   return JsonItem::iterator(L"");
}

JsonItem::iterator& JsonItem::iterator::operator++()
{
   bool end = false;
   std::wstring name;
   JValue value;
   JResult result = Object_GetNextItem(m_src.c_str(), m_src.length(), m_pos, name, value, end);
   if (result.result)
      m_pos = result.next;
   else
      m_pos = m_src.length();

   return *this;
}

JsonItem JsonItem::iterator::operator*() const
{
   if (m_src.empty() || (m_pos == m_src.length()))
      throw std::overflow_error("invalid iterator");

   bool end = false;
   std::wstring name;
   JValue value;
   JResult result = Object_GetNextItem(m_src.c_str(), m_src.length(), m_pos, name, value, end);
   if (!result.result)
      return JsonItem(L"", TYPE_UNDEFINED);

   std::wstring item(m_src.c_str(), m_pos, value.start - m_pos + value.size);
   return JsonItem(item, value.type);
}

std::wstring JsonItem::Name() const
{
   std::wstring name;
   JValue value;
   Object_GetNextItem_IgnoreParseErrors(m_src.c_str(), m_src.length(), 0, name, value);
   // this have worked before => it must have a name
   assert(!name.empty());
   return name;
}
