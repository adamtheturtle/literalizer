#include <initializer_list>
#include <vector>
#include <cstddef>
int main() {
const auto my_data = std::vector<std::vector<int>>{
    std::vector<int>{1, 2},
    std::vector<int>{},
    std::vector<int>{3, 4},
};
    (void)my_data;
    return 0;
}
