#include <initializer_list>
#include <string>
#include <vector>
auto main() -> int {
auto my_data = std::vector<std::string>{
    "C:\\path\\to\\file",
    "back\\\\slash",
    "hello \\\"world\\\"",
    "path\\to \"# file",
    "trailing\\",
    "both \"quotes''' here",
    "line1\\nline2\nwith newline",
};
    (void)my_data;
    return 0;
}
