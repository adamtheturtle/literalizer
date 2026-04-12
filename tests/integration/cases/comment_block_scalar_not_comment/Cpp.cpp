#include <initializer_list>
#include <string>
#include <map>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
static void check_() {
Any my_data = std::map<std::string, std::string>{
    {"description", "# not a comment\n"},
    {"name", "foo"},
};
}
