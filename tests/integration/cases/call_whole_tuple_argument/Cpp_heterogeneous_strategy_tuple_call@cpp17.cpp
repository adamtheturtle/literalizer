#include <tuple>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
process(std::make_tuple("hello", 42, true));
    return 0;
}
