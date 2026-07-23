#include <initializer_list>
#include <string>
#include <vector>
#include <tuple>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
process(std::make_tuple(1, "x"));
    return 0;
}
