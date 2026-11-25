#include <cmath>
#include <map>
#include <string>
int main() {
auto std = std::map<std::string, double>{
    {"nan", static_cast<double>(NAN)},
    {"positive", static_cast<double>(INFINITY)},
    {"negative", -static_cast<double>(INFINITY)},
};
    (void)std;
    return 0;
}
