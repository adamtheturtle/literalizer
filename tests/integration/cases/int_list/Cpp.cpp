#include <initializer_list>
#include <vector>
int main() {
const auto my_data = std::vector<int>{
    1,
    2,
    3,
};
    (void)my_data;
    return 0;
}
