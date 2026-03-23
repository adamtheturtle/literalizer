#include <string>
#include <vector>
void _check() {
auto my_data = std::vector<std::string>{
    "line1\r\nline2",
    "line1\rline2",
    "",
};
my_data = std::vector<std::string>{
    "line1\r\nline2",
    "line1\rline2",
    "",
};
}
