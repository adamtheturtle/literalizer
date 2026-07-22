#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
struct Record0 { std::string name; std::nullptr_t score{}; int age{}; };
int main() {
auto my_data = Record0{
    "Alice",
    nullptr,
    30,
};
(void)my_data;
my_data = Record0{
    "Alice",
    nullptr,
    30,
};
    (void)my_data;
    return 0;
}
