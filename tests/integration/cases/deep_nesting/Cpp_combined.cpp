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
Any my_data = std::map<std::string, std::map<std::string, Any>>{
    {"level1", {{"level2", {{"level3", std::map<std::string, std::map<std::string, Any>>{{"level4", {{"value", "deep"}, {"items", std::vector<std::string>{"a", "b"}}}}}}, {"sibling", 42}}}, {"tags", std::vector<std::map<std::string, Any>>{{{"name", "tag1"}, {"meta", {{"priority", 1}, {"labels", std::vector<std::string>{"x", "y"}}}}}}}}},
};
my_data = std::map<std::string, std::map<std::string, Any>>{
    {"level1", {{"level2", {{"level3", std::map<std::string, std::map<std::string, Any>>{{"level4", {{"value", "deep"}, {"items", std::vector<std::string>{"a", "b"}}}}}}, {"sibling", 42}}}, {"tags", std::vector<std::map<std::string, Any>>{{{"name", "tag1"}, {"meta", {{"priority", 1}, {"labels", std::vector<std::string>{"x", "y"}}}}}}}}},
};
}
