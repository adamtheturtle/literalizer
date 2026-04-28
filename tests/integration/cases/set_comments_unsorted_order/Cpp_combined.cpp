#include <initializer_list>
#include <string>
auto main() -> int {
auto my_data = std::initializer_list<std::string>{
    // before apple
    "apple",
    "banana",  // banana inline
    // trailing
};
(void)my_data;
my_data = std::initializer_list<std::string>{
    // before apple
    "apple",
    "banana",  // banana inline
    // trailing
};
    (void)my_data;
    return 0;
}
