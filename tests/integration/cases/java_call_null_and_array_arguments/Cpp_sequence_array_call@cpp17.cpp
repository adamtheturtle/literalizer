#include <array>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
process(nullptr);
process(std::array<int, 2>{1, 2});
    return 0;
}
