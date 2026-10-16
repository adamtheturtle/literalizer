#include <initializer_list>
#include <vector>
#include <utility>
int main() {
auto item = std::vector<int>{
    1,
    2,
};
auto my_data = std::vector<int>{
    1,
    2,
};
(void)my_data;
my_data = std::move(item);
(void)my_data;
    return 0;
}
