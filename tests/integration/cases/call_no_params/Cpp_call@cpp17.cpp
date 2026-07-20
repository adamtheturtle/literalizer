#include <initializer_list>
#include <vector>
#include <cstddef>
#include <variant>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
process();
process();
    return 0;
}
