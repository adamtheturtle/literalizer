#include <initializer_list>
#include <string>
#include <map>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
int main() {
auto my_data = std::vector<std::map<std::string, LiteralizerVariant<std::string, bool>>>{
    std::map<std::string, LiteralizerVariant<std::string, bool>>{{"type", "create"}, {"pr_id", "pr_1"}, {"draft", true}},
    std::map<std::string, LiteralizerVariant<std::string, bool>>{{"type", "create"}, {"pr_id", "pr_2"}},
};
(void)my_data;
my_data = std::vector<std::map<std::string, LiteralizerVariant<std::string, bool>>>{
    std::map<std::string, LiteralizerVariant<std::string, bool>>{{"type", "create"}, {"pr_id", "pr_1"}, {"draft", true}},
    std::map<std::string, LiteralizerVariant<std::string, bool>>{{"type", "create"}, {"pr_id", "pr_2"}},
};
    (void)my_data;
    return 0;
}
