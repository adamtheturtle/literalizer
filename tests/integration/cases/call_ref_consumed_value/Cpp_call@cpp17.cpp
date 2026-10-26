#include <vector>
#include <utility>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto item = std::vector<int>{
    1,
    2,
};
process(std::move(item));
    return 0;
}
