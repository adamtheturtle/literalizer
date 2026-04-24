#include <initializer_list>
#include <string>
void check_() {
auto my_data = std::initializer_list<std::string>{
    "apple",  // inline comment
    // before banana
    "banana",
    // trailing
};
    (void)my_data;
}
