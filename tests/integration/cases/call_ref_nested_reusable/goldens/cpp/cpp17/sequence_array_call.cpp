#include <array>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto item = std::array<int, 2>{
    1,
    2,
};
process(std::array<std::array<int, 2>, 2>{item, item});
    return 0;
}
