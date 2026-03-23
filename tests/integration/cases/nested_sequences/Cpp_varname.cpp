#include <vector>
void _check() {
auto my_data = std::vector<std::vector<std::vector<int>>>{
    std::vector<std::vector<int>>{std::vector<int>{1, 2}, std::vector<int>{3, 4}},
    std::vector<std::vector<int>>{std::vector<int>{5}},
};
}
