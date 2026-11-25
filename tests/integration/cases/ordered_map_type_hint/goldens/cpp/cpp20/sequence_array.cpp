#include <array>
#include <string>
#include <utility>
#include <vector>
int main() {
auto my_data = std::vector<std::pair<std::string, std::array<int, 2>>>{
    {"a", std::array<int, 2>{1, 2}},
};
    (void)my_data;
    return 0;
}
