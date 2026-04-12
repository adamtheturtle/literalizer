#include <initializer_list>
#include <string>
#include <map>
namespace {
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
}  // namespace
static void check_() {
Any my_data = std::map<std::string, std::string>{
    {"1", "one"},
    {"2", "two"},
    {"42", "answer"},
};
}
