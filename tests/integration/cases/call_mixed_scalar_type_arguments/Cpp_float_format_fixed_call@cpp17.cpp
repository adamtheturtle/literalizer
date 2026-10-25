#include <initializer_list>
#include <string>
#include <cmath>
#include <vector>
#include <variant>
template <typename... Args> auto capture(Args...) { return 0; }
int main() {
capture(static_cast<double>(NAN), static_cast<double>(INFINITY), -static_cast<double>(INFINITY), 1.250000, "2024-01-15", "2024-01-15T12:34:56", "[ordinary text]");
    return 0;
}
