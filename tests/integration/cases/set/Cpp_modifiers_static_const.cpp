#include <initializer_list>
#include <string>
void check_() {
static const auto my_data = std::initializer_list<std::string>{
    "apple",
    "banana",
    "cherry",
};
}
