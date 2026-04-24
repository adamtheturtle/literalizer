#include <initializer_list>
#include <cmath>
#include <vector>
void check_() {
auto my_data = std::vector<double>{
    static_cast<double>(INFINITY),
    -static_cast<double>(INFINITY),
    static_cast<double>(NAN),
};
my_data = std::vector<double>{
    static_cast<double>(INFINITY),
    -static_cast<double>(INFINITY),
    static_cast<double>(NAN),
};
}
