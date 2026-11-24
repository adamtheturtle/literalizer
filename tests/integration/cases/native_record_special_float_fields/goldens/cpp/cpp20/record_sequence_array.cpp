#include <cmath>
struct Record0 { double positive{}; double negative{}; double nan_value{}; double finite{}; };
int main() {
auto my_data = Record0{
    .positive = static_cast<double>(INFINITY),
    .negative = -static_cast<double>(INFINITY),
    .nan_value = static_cast<double>(NAN),
    .finite = 1.5,
};
    (void)my_data;
    return 0;
}
