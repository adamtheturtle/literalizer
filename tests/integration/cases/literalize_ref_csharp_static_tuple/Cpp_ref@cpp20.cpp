#include <initializer_list>
#include <vector>
#include <utility>
int main() {
auto ref_data = std::vector<int>{
    1,
    2,
};
static auto my_data = std::move(ref_data);
    (void)my_data;
    return 0;
}
