#include <initializer_list>
#include <vector>
#include <variant>
int main() {
auto existing = 1;
auto my_data = std::vector<std::variant<int, std::vector<std::vector<int>>>>{
    0,
    std::vector<std::vector<int>>{std::vector<int>{existing}},
};
    (void)my_data;
    return 0;
}
