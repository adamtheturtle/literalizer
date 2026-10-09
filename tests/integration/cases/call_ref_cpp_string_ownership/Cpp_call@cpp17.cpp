#include <initializer_list>
#include <string>
#include <vector>
template <typename... Args> auto consume(Args...) { return 0; }
int main() {
const auto* item = "s";
consume(item);
    return 0;
}
