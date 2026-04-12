#include <initializer_list>
#include <string>
#include <map>
namespace {
struct Any {
    template<class T> Any(T&& /*unused*/) noexcept {}
    Any(std::initializer_list<Any> /*unused*/) noexcept {}
};
}  // namespace
static void check_() {
Any my_data = std::map<std::string, std::string>{
    {"key", "value \" # not a comment"},  // real
};
my_data = std::map<std::string, std::string>{
    {"key", "value \" # not a comment"},  // real
};
}
