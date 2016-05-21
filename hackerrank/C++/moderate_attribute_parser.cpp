/* 
   https://www.hackerrank.com/challenges/attribute-parser
      parsing for attributes, this is only moderate !!!
   tag_parser
*/

#include <assert.h>
#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;

inline static
size_t find_close(const string& text, size_t start, const string& tag)
{
   string tagged = "</"; tagged += tag; tagged += '>';
   return text.find(tagged, start);
}

inline static
bool update_tag(const string& text, size_t start, const string& tag, string& lasttag)
{
   if (!lasttag.empty())
   {
      size_t prev_close_tag = find_close(text, start, lasttag);
      if (prev_close_tag == string::npos)  // already closed
         return false;

      size_t close_tag = find_close(text, start, tag);
      if (close_tag == string::npos || close_tag >= prev_close_tag)
         return false;
   }
   lasttag = tag;
   return true;
}

bool is_open_tag(const string& text, size_t start, size_t stop)
{
   size_t pos = start;
   while (pos < stop)
   {
      pos = text.find_first_of('<', pos);
      if (pos == string::npos || pos >= stop)
         return false;
      if ('/' == text[pos+1])
      {
         pos += 2;
         continue;
      }

      size_t next = text.find_first_of(" >", pos);
      if (next == string::npos || next >= stop)
         return false;

      string tag = text.substr(pos+1, next-pos-1);
      string tagged = "</"; tagged += tag; tagged += '>';

      pos = next+1;
      next = text.find(tagged, pos);
      if (next == string::npos || next >= stop)
         return true;
   }

   return false;
}

bool solve_query(const string& text, const string& query, string& result)
{
   assert(result.empty());

   size_t pos = 0, prev = 0, in = 0;
   string lasttag;
   for (pos = query.find_first_of("~."); string::npos != pos && query[pos] == '.'; 
      prev = pos+1, pos = query.find_first_of("~.", prev))
   {
      string tag(query.substr(prev, pos-prev));

      string tagged("<"); tagged += tag;
      const size_t prev_in = in;
      in = text.find(tagged, in);
      if (in == string::npos)
         return false;
      in += tagged.length();

      if (!update_tag(text, in, tag, lasttag))
         return false;
      if (is_open_tag(text, prev_in, in))
         return false;
   }

   if (string::npos == pos)
      return false;
   assert (query[pos] == '~');
   if (!update_tag(text, in, query.substr(prev, pos-prev), lasttag))
      return false;
   string attribute = query.substr(pos+1);
   if (attribute.empty())
      return false;

   string tagged("<"); tagged += lasttag;
   prev = in;
   in = text.find(tagged, in);
   if (in == string::npos)
      return false;
   if (is_open_tag(text, prev, in))
      return false;
   in += tagged.length();

   tagged = "</"; tagged += lasttag; tagged += '>';
   const size_t close_tag = text.find(tagged, in);
   if (close_tag == string::npos)
      return false;

   tagged = " "; tagged += attribute; tagged += ' ';
   prev = in;
   in = text.find(tagged, in);
   if (in == string::npos || in >= close_tag)
      return false;
   if (is_open_tag(text, prev, in+1))
      return false;

   in += tagged.length();
   in = text.find_first_of('=', in);
   if (in == string::npos || in >= close_tag)
      return false;
   ++in;
   
   in = text.find_first_of('\"', in);
   if (in == string::npos || in >= close_tag)
      return false;
   prev = in;
   in = text.find_first_of("\">", prev+1);
   if (in == string::npos || in >= close_tag)
      return false;

   result = text.substr(prev+1, in-prev-1);

   return true;
}

string solve_query(const string& text, const string& query)
{
   string result;
   return solve_query(text, query, result) ? result : "Not Found!";
}

void read_and_solve()
{
   int no_lines, no_queris;
   cin>>no_lines>>no_queris;
   char line[200+1+1];
   line[sizeof(line)-1] = '\0';
   cin.getline(line, sizeof(line)-2); // finish the line
   string text;
   for (int i = 0; i < no_lines; ++i)
   {        
      cin.getline(line, sizeof(line)-2);
      text += line;
   }
   for (int i = 0; i < no_queris; ++i)
   {   
      cin.getline(line, sizeof(line)-2);
      string query(line);
      string result(solve_query(text, query));
      cout<<result.c_str()<<endl;
   }
}

void debug_validations_2()
{
   const char* text = "<a value = \"GoodVal\">\
                      <b value = \"BadVal\" size = \"10\">\
                      </b>\
                      <c height = \"auto\">\
                      <d size = \"3\">\
                      <e strength = \"2\">\
                      </e>\
                      </d>\
                      </c>\
                      </a>";

   string result = solve_query(text, "a~value");
   assert (0 == result.compare("GoodVal"));
   result = solve_query(text, "b~value");
   assert (0 == result.compare("Not Found!"));
   result = solve_query(text, "a.b~size");
   assert (0 == result.compare("10"));
   result = solve_query(text, "a.b~value");
   assert (0 == result.compare("BadVal"));
   result = solve_query(text, "a.b.c~height");
   assert (0 == result.compare("Not Found!"));
   result = solve_query(text, "a.c~height");
   assert (0 == result.compare("auto"));
   result = solve_query(text, "a.d.e~strength");
   assert (0 == result.compare("Not Found!"));
   result = solve_query(text, "a.c.d.e~strength");
   assert (0 == result.compare("2"));
   result = solve_query(text, "d~sze");
   assert (0 == result.compare("Not Found!"));
   result = solve_query(text, "d~size");
   assert (0 == result.compare("Not Found!"));
   result = solve_query(text, "a.c.d~size");
   assert (0 == result.compare("3"));
}

void debug_validations_1()
{
   const char* text = "<tag1 value = \"HelloWorld\">\
                      <tag2 name = \"Name1\">\
                      </tag2>\
                      </tag1>";
   string result = solve_query(text, "tag1.tag2~name");
   assert (0 == result.compare("Name1"));
   result = solve_query(text, "tag1~name");
   assert (0 == result.compare("Not Found!"));
   result = solve_query(text, "tag1~value");
   assert (0 == result.compare("HelloWorld"));
}

void debug_validations_3()
{
   const char* text = "<tag1 v1 = \"123\" v2 = \"43.4\" v3 = \"hello\">\
                      </tag1>\
                      <tag2 v4 = \"v2\" name = \"Tag2\">\
                      <tag3 v1 = \"Hello\" v2 = \"World!\">\
                      </tag3>\
                      <tag4 v1 = \"Hello\" v2 = \"Universe!\">\
                      </tag4>\
                      </tag2>\
                      <tag5>\
                      <tag7 new_val = \"New\">\
                      </tag7>\
                      </tag5>\
                      <tag6>\
                      <tag8 intval = \"34\" floatval = \"9.845\">\
                      </tag8>\
                      </tag6>";

   static const struct 
   {
      string query;
      const char* result;
   }
   queries[] =
   {
      {"tag1~v1", "123"},
      {"tag1.v1", "Not Found!"},
      {"tag1~v2", "43.4"},
      {"tag1~v3", "hello"},
      {"tag4~v2", "Not Found!"},
      {"tag2.tag4~v1", "Hello"},
      {"tag2.tag4~v2", "Universe!"},
      {"tag2.tag3~v2", "World!"},
      {"tag5.tag7~new_val", "New"},
      {"tag5~new_val", "Not Found!"},
      {"tag7~new_val", "Not Found!"},
      {"tag6.tag8~intval", "34"},
      {"tag6.tag8~floatval", "9.845"},
      {"tag6.tag8~val", "Not Found!"},
      {"tag8~intval", "Not Found!"},
   };

   for (auto query : queries)
   {
      string result = solve_query(text, query.query);
      assert(0 == result.compare(query.result));
   }

   printf("");
}

void debug_validations()
{   
   debug_validations_1();
   debug_validations_2();
   debug_validations_3();
}

int removePrefixFor_main() 
{
   const char* text = "<tag1 v1 = \"123\" v2 = \"43.4\" v3 = \"hello\">\
                      </tag1>\
                      <tag2 v4 = \"v2\" name = \"Tag2\">\
                      <tag3 v1 = \"Hello\" v2 = \"World!\">\
                      </tag3>\
                      <tag4 v1 = \"Hello\" v2 = \"Universe!\">\
                      </tag4>\
                      </tag2>\
                      <tag5>\
                      <tag7 new_val = \"New\">\
                      </tag7>\
                      </tag5>\
                      <tag6>\
                      <tag8 intval = \"34\" floatval = \"9.845\">\
                      </tag8>\
                      </tag6>";

   string result = solve_query(text, "tag6.tag8~intval");

   debug_validations();
   //read_and_solve();

   return 0;
}
