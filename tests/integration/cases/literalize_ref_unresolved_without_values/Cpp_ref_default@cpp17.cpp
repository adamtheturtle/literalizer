#include <utility>
#include <vector>
#include <cstdlib>
int main() {
auto a = 0;
auto my_data = std::vector<int>{
    std::move_if_noexcept(a),
    1,
};
auto expected_data = std::vector<int>{
    0,
    1,
};
((my_data) != (expected_data) ? std::abort() : static_cast<void>(0));
    return 0;
}
