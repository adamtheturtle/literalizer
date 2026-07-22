#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
struct Record0 { std::string s; int i{}; double f{}; bool b{}; std::nullptr_t n{}; std::string d; std::string dt; std::string by; };
int main() {
auto my_data = Record0{
    "string",
    1,
    1.5,
    true,
    nullptr,
    "2024-01-15",
    "2024-01-15T12:00:00",
    "48656c6c6f",
};
(void)my_data;
my_data = Record0{
    "string",
    1,
    1.5,
    true,
    nullptr,
    "2024-01-15",
    "2024-01-15T12:00:00",
    "48656c6c6f",
};
    (void)my_data;
    return 0;
}
