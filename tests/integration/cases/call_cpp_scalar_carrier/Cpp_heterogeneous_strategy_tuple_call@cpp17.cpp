#include <initializer_list>
#include <string>
#include <cstddef>
#include <vector>
#include <variant>
#include <tuple>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
process("hello");
process(42);
process(true);
process(nullptr);
    return 0;
}
