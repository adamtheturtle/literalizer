#include <cmath>
template <typename... Args> auto capture(Args...) { return 0; }
int main() {
capture(static_cast<double>(NAN), static_cast<double>(INFINITY), -static_cast<double>(INFINITY), 1.25, "2024-01-15", 1705322096, "[ordinary text]");
    return 0;
}
