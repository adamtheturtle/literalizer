#include <initializer_list>
#include <string>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
template <typename... Args> auto process(Args...) { return 0; }
int main() {
process("hello");
process(42);
process(true);
    return 0;
}
