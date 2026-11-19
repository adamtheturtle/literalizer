#include <vector>
#include <utility>
#include <cstdlib>
int main() {
auto missing = std::vector<int>{
    1,
    2,
};
auto&& my_data = std::move_if_noexcept(missing);
auto expected_data = std::vector<int>{
    1,
    2,
};
((my_data) != (expected_data) ? std::abort() : static_cast<void>(0));
    return 0;
}
