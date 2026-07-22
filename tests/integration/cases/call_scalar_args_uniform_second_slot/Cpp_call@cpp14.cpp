#include <initializer_list>
#include <string>
#include <vector>
#include <tuple>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
process("hello", "a");
process(42, "b");
process(true, "c");
    return 0;
}
