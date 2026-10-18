#include <initializer_list>
#include <vector>
#include <cstddef>
#include <variant>
int main() {
auto my_data = std::vector<std::vector<std::vector<int>>>{
    std::vector<std::vector<int>>{std::vector<int>{1}},
    std::vector<std::vector<int>>{std::vector<int>{}},
};
    (void)my_data;
    return 0;
}
