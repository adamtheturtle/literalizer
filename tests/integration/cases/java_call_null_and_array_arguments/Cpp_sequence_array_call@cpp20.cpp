#include <initializer_list>
#include <cstddef>
#include <array>
#include <variant>
auto process(auto...) { return 0; }
int main() {
process(nullptr);
process(std::array<int, 2>{1, 2});
    return 0;
}
