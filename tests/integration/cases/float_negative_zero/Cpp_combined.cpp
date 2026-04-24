#include <initializer_list>
#include <vector>
void check_() {
auto my_data = std::vector<double>{
    -0.0,
    1.5,
};
(void)my_data;
my_data = std::vector<double>{
    -0.0,
    1.5,
};
    (void)my_data;
}
