#include <initializer_list>
#include <vector>
void check_() {
auto my_data = std::vector<double>{
    1,
    2.5,
    3,
};
(void)my_data;
my_data = std::vector<double>{
    1,
    2.5,
    3,
};
    (void)my_data;
}
