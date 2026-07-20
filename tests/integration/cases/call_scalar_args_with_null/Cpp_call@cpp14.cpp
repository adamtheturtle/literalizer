#include <initializer_list>
#include <string>
#include <cstddef>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
template <typename... Args> auto process(Args...) { return 0; }
int main() {
process(nullptr);
process("hello");
    return 0;
}
