#include <cmath>
struct Record0 { double nan{}; double positive{}; double negative{}; };
int main() {
auto std = Record0{
    static_cast<double>(NAN),
    static_cast<double>(INFINITY),
    -static_cast<double>(INFINITY),
};
    (void)std;
    return 0;
}
