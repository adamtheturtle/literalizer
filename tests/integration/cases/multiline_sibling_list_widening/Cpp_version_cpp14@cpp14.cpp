#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <utility>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
int main() {
auto my_data = std::map<std::string, LiteralizerVariant<std::vector<std::pair<std::string, int>>, std::map<std::string, LiteralizerVariant<std::vector<int>, std::vector<std::string>>>, std::vector<std::string>>>{
    {"omap_value", std::vector<std::pair<std::string, int>>{{"first", 1}}},
    {"sibling_lists", std::map<std::string, LiteralizerVariant<std::vector<int>, std::vector<std::string>>>{{"numbers", std::vector<int>{1, 2}}, {"strings", std::vector<std::string>{"x", "y"}}}},
    {"ref_marker_present", std::vector<std::string>{"$keep", "z"}},
};
    (void)my_data;
    return 0;
}
