
#include <iostream>
#include <sstream>
#include <cassert>

#include "JsonParser.h"

//void TestUnit_1()
//{
//    JsonItem item;
//    for (JsonItem::iterator it = item.begin(); it != item.end(); ++it)
//    {
//        switch (it.Type())
//        {
//        case TYPE_STRING:
//            {
//                //JsonValueString value = *it;
//                //JsonValueString value = it.operator*<TYPE_STRING, std::string>();
//            }
//            break;
//        }
//    }
//}

void TestUnit_2_Array()
{
    static const wchar_t* test =
    {
        L"{   \"names\" : [\"Onze\", \"Treize\", \"Cinquante\", \"Quatre vingt\"]}"
    };

    std::wstringbuf buf(test);
    std::wistream ss(&buf);

    JsonParser item(ss);
    size_t i = 0;
    for (JsonItem::iterator it = item.begin(); it != item.end(); ++it, ++i)
    {
       JsonItem item(*it);
       //wprintf(L"Item: %s\n", item.Name().c_str());
    }
    assert(1 == i);
}

void TestUnit_3_just_begin()
{
   static const wchar_t* test =
   {
      L"{\
       \"firstName\": \"John\",\
       \"lastName\": \"Smith\"\
       }"
   };

   std::wstringbuf buf(test);
   std::wistream ss(&buf);

   JsonParser parser(ss);
   JsonItem::iterator it = parser.begin();
   assert(it != parser.end());
}

void TestUnit_4_just_begin()
{
   static const wchar_t* test =
   {
      L"{\
       \"firstName\": \"Balthzar\",\
       \"lastName\": \"Carolyn\",\
       \"others\": {\
       \"firstName\": \"Cairo\",\
       \"lastName\": \"Vangelis\"\
       }\
       }"
   };

   std::wstringbuf buf(test);
   std::wistream ss(&buf);

   JsonParser parser(ss);
   JsonItem::iterator it = parser.begin();
   assert(it != parser.end());
}

void TestUnit_5_a_for()
{
   static const wchar_t* test =
   {
      L"{\
       \"firstName\": \"Jennifer\",\
       \"lastName\": \"Connelly\",\
       \"others\": {\
       \"firstName\": \"Baghdad\",\
       \"lastName\": \"Tlemcen\"\
       }\
       }"
   };

   std::wstringbuf buf(test);
   std::wistream ss(&buf);

   JsonParser parser(ss);
   size_t i = 0;
   for (JsonItem::iterator it = parser.begin(); it != parser.end(); ++it, ++i);
   assert(3 == i);
}

void TestUnit_6_a_for_complete()
{
   static const wchar_t* test =
   {
      L"{\
       \"firstName\": \"Wolfgang\",\
       \"someName\": \"Amadeus\",\
       \"lastName\": \"Mozart\",\
       \"othersName\": {\
       \"firstName\": \"Beethoven\",\
       \"lastName\": \"Chopin\"\
       }\
       }"
   };

   std::wstringbuf buf(test);
   std::wistream ss(&buf);

   JsonParser parser(ss);
   size_t i = 0;
   for (JsonItem::iterator it = parser.begin(); it != parser.end(); ++it, ++i)
   {
      JsonItem item(*it);
      //wprintf(L"Item: %s\n", item.Name().c_str());
      assert(std::wstring::npos != item.Name().find(L"Name"));
   }
   assert(4 == i);
}

void TestUnits()
{
   //  TODO
   //TestUnit_1();
   
   // done
   TestUnit_2_Array();
   TestUnit_3_just_begin();
   TestUnit_4_just_begin();

   TestUnit_5_a_for();
   TestUnit_6_a_for_complete();
}