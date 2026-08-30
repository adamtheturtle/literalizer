#include <initializer_list>
#include <vector>
#include <cstddef>
int main() {
auto a = std::vector<int>{};
auto b = std::vector<int>{
    1,
};
auto my_data = std::vector<std::vector<int>>{
    std::move(a),
    std::move(b),
};
    (void)my_data;
    return 0;
}
