#include <initializer_list>
#include <cmath>
#include <vector>
void check_() {
auto my_data = std::vector<double>{
    static_cast<double>(INFINITY),
    -static_cast<double>(INFINITY),
    static_cast<double>(NAN),
};
(void)my_data;
my_data = std::vector<double>{
    static_cast<double>(INFINITY),
    -static_cast<double>(INFINITY),
    static_cast<double>(NAN),
};
    (void)my_data;
}
