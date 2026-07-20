#include <initializer_list>
#include <string>
#include <map>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
int main() {
auto my_data = std::map<std::string, LiteralizerVariant<std::string, std::map<std::string, LiteralizerVariant<int, std::string, bool, std::vector<int>>>>>{
    {"project", "alpha"},
    {"lead_task", std::map<std::string, LiteralizerVariant<int, std::string, bool, std::vector<int>>>{{"id", 100}, {"description", "first task"}, {"is_done", false}, {"blocks", std::vector<int>{102, 103}}}},
};
(void)my_data;
my_data = std::map<std::string, LiteralizerVariant<std::string, std::map<std::string, LiteralizerVariant<int, std::string, bool, std::vector<int>>>>>{
    {"project", "alpha"},
    {"lead_task", std::map<std::string, LiteralizerVariant<int, std::string, bool, std::vector<int>>>{{"id", 100}, {"description", "first task"}, {"is_done", false}, {"blocks", std::vector<int>{102, 103}}}},
};
    (void)my_data;
    return 0;
}
