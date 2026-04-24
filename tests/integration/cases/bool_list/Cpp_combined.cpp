#include <initializer_list>
#include <vector>
void check_() {
auto my_data = std::vector<bool>{
    true,
    false,
    true,
};
(void)my_data;
my_data = std::vector<bool>{
    true,
    false,
    true,
};
    (void)my_data;
}
