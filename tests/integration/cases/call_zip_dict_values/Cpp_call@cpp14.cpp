#include <initializer_list>
#include <string>
#include <map>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
template <typename... Args> auto process(Args...) { return 0; }
template <typename... Args> auto emit(Args...) { return 0; }
int main() {
emit(process("hello"), std::map<std::string, int>{{"a", 1}, {"b", 2}});
emit(process(42), std::map<std::string, int>{{"c", 3}, {"d", 4}});
    return 0;
}
