#include <initializer_list>
#include <vector>
#include <cstddef>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
template <typename... Args> auto process(Args...) { return 0; }
template <typename... Args> auto emit(Args...) { return 0; }
int main() {
emit(process());
emit(process());
    return 0;
}
