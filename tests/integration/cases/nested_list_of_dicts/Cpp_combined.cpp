#include <initializer_list>
#include <string>
#include <map>
#include <vector>
namespace {
struct Any {
    template<class T> Any(T&& /*unused*/) noexcept {}  // NOLINT(google-explicit-constructor,hicpp-explicit-conversions,bugprone-forwarding-reference-overload)
    Any(std::initializer_list<Any> /*unused*/) noexcept {}  // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
}  // namespace
static void check_() {
Any my_data = std::vector<std::vector<std::map<std::string, std::string>>>{
    std::vector<std::map<std::string, std::string>>{std::map<std::string, std::string>{{"name", "Alice"}}, std::map<std::string, std::string>{{"name", "Bob"}}},
    std::vector<std::map<std::string, std::string>>{std::map<std::string, std::string>{{"name", "Charlie"}}, std::map<std::string, std::string>{{"name", "Dave"}}},
};
my_data = std::vector<std::vector<std::map<std::string, std::string>>>{
    std::vector<std::map<std::string, std::string>>{std::map<std::string, std::string>{{"name", "Alice"}}, std::map<std::string, std::string>{{"name", "Bob"}}},
    std::vector<std::map<std::string, std::string>>{std::map<std::string, std::string>{{"name", "Charlie"}}, std::map<std::string, std::string>{{"name", "Dave"}}},
};
}
