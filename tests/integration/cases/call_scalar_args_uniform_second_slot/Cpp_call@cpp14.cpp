#include <initializer_list>
#include <string>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
template <typename... Args> auto process(Args...) { return 0; }
int main() {
process("hello", "a");
process(42, "b");
process(true, "c");
    return 0;
}
