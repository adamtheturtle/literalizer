#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
template <typename... Args> auto process(Args...) { return 0; }
template <typename... Args> auto emit(Args...) { return 0; }
int main() {
emit(process("hello"), "one");
emit(process(42), "zero");
    return 0;
}
