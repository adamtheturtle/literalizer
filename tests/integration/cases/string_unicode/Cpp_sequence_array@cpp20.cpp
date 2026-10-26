#include <initializer_list>
#include <string>
#include <array>
int main() {
auto my_data = std::array<std::string, 3>{
    "café",
    "中文",
    "😀",
};
    (void)my_data;
    return 0;
}
