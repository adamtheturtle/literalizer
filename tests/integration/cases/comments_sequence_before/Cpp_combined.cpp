#include <initializer_list>
#include <string>
#include <vector>
void check_() {
auto my_data = std::vector<std::string>{
    // first
    "a",
    // second
    "b",
};
(void)my_data;
my_data = std::vector<std::string>{
    // first
    "a",
    // second
    "b",
};
    (void)my_data;
}
