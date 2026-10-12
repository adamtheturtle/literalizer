#include <initializer_list>
#include <string>
#include <cmath>
struct Record0 { double nan{}; double positive{}; double negative{}; };
int main() {
auto std = Record0{
    .nan = static_cast<double>(NAN),
    .positive = static_cast<double>(INFINITY),
    .negative = -static_cast<double>(INFINITY),
};
    (void)std;
    return 0;
}
