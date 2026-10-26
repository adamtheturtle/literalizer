#include <array>
int main() {
auto my_data = std::array<double, 3>{
    5.0e-324,
    -5.0e-324,
    1.0e-310,
};
    (void)my_data;
    return 0;
}
