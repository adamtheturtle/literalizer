#include <cmath>
#include <string>
#include <unordered_map>
int main() {
auto my_data = std::unordered_map<std::string, double>{
    {"positive", static_cast<double>(INFINITY)},
    {"negative", -static_cast<double>(INFINITY)},
    {"nan_value", static_cast<double>(NAN)},
    {"finite", 1.5},
};
    (void)my_data;
    return 0;
}
