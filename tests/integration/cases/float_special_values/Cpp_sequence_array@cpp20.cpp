#include <initializer_list>
#include <cmath>
#include <array>
int main() {
auto my_data = std::array<double, 3>{
    static_cast<double>(INFINITY),
    -static_cast<double>(INFINITY),
    static_cast<double>(NAN),
};
    (void)my_data;
    return 0;
}
