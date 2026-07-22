#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
struct Record0 { std::string name; int age{}; bool active{}; std::nullptr_t score{}; std::string joined; std::string last_login; std::string avatar; };
int main() {
auto my_data = Record0{
    "Alice",
    30,
    true,
    nullptr,
    "2024-01-15",
    "2024-01-15T12:30:00+00:00",
    "48656c6c6f",
};
(void)my_data;
my_data = Record0{
    "Alice",
    30,
    true,
    nullptr,
    "2024-01-15",
    "2024-01-15T12:30:00+00:00",
    "48656c6c6f",
};
    (void)my_data;
    return 0;
}
