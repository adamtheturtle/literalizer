#include <initializer_list>
#include <vector>
int main() {
static auto my_data = std::vector<int>{
    1,
    2,
};
    (void)my_data;
    return 0;
}
