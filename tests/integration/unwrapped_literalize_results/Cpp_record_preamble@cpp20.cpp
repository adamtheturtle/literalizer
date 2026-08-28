#include <initializer_list>
#include <string>
#include <variant>
struct Record0 { int a{}; std::string b; };
Record0{
    .a = 1,
    .b = "x",
}
