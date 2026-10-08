#include <initializer_list>
#include <vector>
int main() {
auto ref_data = std::vector<int>{
    1,
    2,
};
static auto my_data = ref_data;
    (void)my_data;
    return 0;
}
