#include <initializer_list>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::string>{
    "line1\r\nline2",
    "line1\rline2",
    "",
};
(void)my_data;
my_data = std::vector<std::string>{
    "line1\r\nline2",
    "line1\rline2",
    "",
};
    (void)my_data;
    return 0;
}
