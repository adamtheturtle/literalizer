#include <initializer_list>
#include <string>
void check_() {
auto my_data = std::initializer_list<std::string>{
    "apple",
    "banana",
    "cherry",
};
my_data = std::initializer_list<std::string>{
    "apple",
    "banana",
    "cherry",
};
}
