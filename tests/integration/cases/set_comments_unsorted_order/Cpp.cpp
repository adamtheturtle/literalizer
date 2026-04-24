#include <initializer_list>
#include <string>
void check_() {
auto my_data = std::initializer_list<std::string>{
    // before apple
    "apple",
    "banana",  // banana inline
    // trailing
};
    (void)my_data;
}
