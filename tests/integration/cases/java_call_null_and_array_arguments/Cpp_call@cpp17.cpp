#include <initializer_list>
#include <cstddef>
#include <vector>
#include <variant>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
process(nullptr);
process(std::vector<int>{1, 2});
    return 0;
}
