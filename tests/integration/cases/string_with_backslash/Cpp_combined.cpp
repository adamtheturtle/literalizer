#include <initializer_list>
#include <string>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
void check_() {
auto my_data = std::vector<std::string>{
    "C:\\path\\to\\file",
    "back\\\\slash",
    "hello \\\"world\\\"",
    "path\\to \"# file",
    "trailing\\",
    "both \"quotes''' here",
    "line1\\nline2\nwith newline",
};
my_data = std::vector<std::string>{
    "C:\\path\\to\\file",
    "back\\\\slash",
    "hello \\\"world\\\"",
    "path\\to \"# file",
    "trailing\\",
    "both \"quotes''' here",
    "line1\\nline2\nwith newline",
};
}
