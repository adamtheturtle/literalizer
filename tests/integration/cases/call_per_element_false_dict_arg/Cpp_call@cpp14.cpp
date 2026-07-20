#include <initializer_list>
#include <string>
#include <map>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
template <typename... Args> auto process(Args...) { return 0; }
int main() {
process(std::map<std::string, LiteralizerVariant<int, std::string>>{{"a", 1}, {"b", "x"}});
    return 0;
}
