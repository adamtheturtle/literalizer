#include <initializer_list>
#include <string>
#include <array>
#include <utility>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::pair<std::string, std::array<int, 2>>>{
    {"a", std::array<int, 2>{1, 2}},
};
    (void)my_data;
    return 0;
}
