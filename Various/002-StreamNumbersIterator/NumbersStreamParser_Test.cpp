
#include <cassert>
#include <sstream>
#include <iostream> //cout

#include "NumbersStreamParser.h"

void FileNumbersParser_Test_Invalids()
{
    static const char* test[] =
    {
        "\
            123\
            -54\
        "
        "",
        "fides",
        "--3",
        "-1000000001",
        "+1000000001",
        "3 45",
    };
    for (size_t i = 0; i < sizeof(test)/sizeof(test[0]); ++i)
    {
        std::stringbuf buf(test[i]);
        std::istream ss(&buf);

        Solution sol(ss);
        Solution::iterator it = sol.begin();
        assert(it == sol.end());
    }
}

void FileNumbersParser_Test_Valids_1line()
{
    static const char* test[] =
    {
        "\
            123\n\
            -5y4\n\
        ",
        "-3",
        "3",
        "+3",
        "+0000000000003",
        "0000000000003",
        " 03   \t",
        "-030",
        "+0999999999",
        "-0999999999",
        "-1000000000",
        "+1000000000"
    };
    for (size_t i = 0; i < sizeof(test)/sizeof(test[0]); ++i)
    {
        std::stringbuf buf(test[i]);
        std::istream ss(&buf);

        Solution sol(ss);
        Solution::iterator it = sol.begin();
        assert(it != sol.end());
        ++it;
        assert(it == sol.end());
    }
}

void FileNumbersParser_Test_Valids_2lines()
{
    static const char* test[] =
    {
        "\
            123\n\
            -54\n\
        ",
        "\
            123\n\
            -5.4\n\
            0.1\n\
            00000000000000000\n\
        ",
        "\
            -5\n\
            +0000000000\n\
        ",
    };
    for (size_t i = 0; i < sizeof(test)/sizeof(test[0]); ++i)
    {
        std::stringbuf buf(test[i]);
        std::istream ss(&buf);

        Solution sol(ss);
        Solution::iterator it = sol.begin();
        assert(it != sol.end());
        ++it;
        assert(it != sol.end());
        ++it;
        assert(it == sol.end());
    }
}

void FileNumbersParser_Test_1()
{
    static const char* test = 
    "\
        123\n\
        -54\n\
        haj\n\
        +000000000001\n\
        -4540\n\
        1119\n\
        3232\n\
        +0000004321     \n\
        +2000000000\n\
    ";
    std::stringbuf buf(test);
    std::istream ss(&buf);

    Solution sol(ss);
    for (Solution::iterator it = sol.begin(); it != sol.end(); ++it) {
        int x = *it;
        std::cout << x << std::endl;
    }
}

void FileNumbersParser_Test_Standard()
{
    static const char* test = 
    "\
        137\n\
        -104\n\
        2 58\n\
          +0\n\
        ++3\n\
        +1\n\
         23.9\n\
        2000000000\n\
        -0\n\
        five\n\
         -1\n\
    ";
    std::stringbuf buf(test);
    std::istream ss(&buf);

    int i = 0;
    static const int result[] = {137, -104, 0, 1, 0, -1};

    Solution sol(ss);
    for (Solution::iterator it = sol.begin(); it != sol.end(); ++it, ++i) {
        assert(i < sizeof(result)/sizeof(result[0]));
        assert(result[i] == *it);
    }
}

void FileNumbersParser_Test_Errors()
{
   std::stringbuf buf("");
   std::istream ss(&buf);
   Solution sol(ss);

   int result = -1;
   try
   {
      result = *sol.begin();
   }
   catch (std::exception)
   {
      result = -2;
   }
   assert(-2 == result);
}

void FileNumbersParser_Tests()
{
    FileNumbersParser_Test_Invalids();
    FileNumbersParser_Test_Valids_1line();
    FileNumbersParser_Test_Valids_2lines();
    FileNumbersParser_Test_1();
    FileNumbersParser_Test_Standard();
    FileNumbersParser_Test_Errors();
}
