#include <initializer_list>
#include <string>
#include <vector>
void _check() {
    [[maybe_unused]] _Any _v = std::vector<std::string>{
    "line1\r\nline2",
    "line1\rline2",
    "",
};
}
