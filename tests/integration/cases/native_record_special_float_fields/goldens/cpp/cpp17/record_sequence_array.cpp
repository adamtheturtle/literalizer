#include <cmath>
struct Record0 { double positive{}; double negative{}; double nan_value{}; double finite{}; };
int main() {
auto my_data = Record0{
    static_cast<double>(INFINITY),
    -static_cast<double>(INFINITY),
    static_cast<double>(NAN),
    1.5,
};
    (void)my_data;
    return 0;
}
