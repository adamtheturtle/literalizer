#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
struct Record0 { std::string name; int age{}; bool active{}; std::nullptr_t score{}; };
int main() {
auto my_data = Record0{
    "Alice",
    30,
    true,
    nullptr,
};
(void)my_data;
my_data = Record0{
    "Alice",
    30,
    true,
    nullptr,
};
    (void)my_data;
    return 0;
}
