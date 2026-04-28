#include <initializer_list>
#include <string>
auto main() -> int {
auto my_data = std::initializer_list<std::string>{
    "apple",  // inline comment
    // before banana
    "banana",
    // trailing
};
(void)my_data;
my_data = std::initializer_list<std::string>{
    "apple",  // inline comment
    // before banana
    "banana",
    // trailing
};
    (void)my_data;
    return 0;
}
