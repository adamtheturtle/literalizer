#include <initializer_list>
#include <string>
#include <cstddef>
#include <vector>
#include <variant>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
process(nullptr);
process("hello");
    return 0;
}
