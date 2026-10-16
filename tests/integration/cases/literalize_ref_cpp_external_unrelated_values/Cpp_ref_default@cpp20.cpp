#include <initializer_list>
#include <vector>
#include <utility>
int main() {
auto missing = std::vector<int>{
    1,
    2,
};
auto&& my_data = std::move(missing);
if (my_data != std::vector<int>{1, 2}) { return 1; }
    return 0;
}
