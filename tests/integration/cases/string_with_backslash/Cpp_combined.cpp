#include <initializer_list>
#include <string>
#include <vector>
namespace {
struct Any {
    template<class T> Any(T&& /*unused*/) noexcept {}  // NOLINT(google-explicit-constructor,hicpp-explicit-conversions,bugprone-forwarding-reference-overload)
    Any(std::initializer_list<Any> /*unused*/) noexcept {}  // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
}  // namespace
static void check_() {
Any my_data = std::vector<std::string>{
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
