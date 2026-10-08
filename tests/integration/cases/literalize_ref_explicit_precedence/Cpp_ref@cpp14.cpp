#include <initializer_list>
#include <vector>
int main() {
auto x = std::vector<int>{
    1,
    2,
};
auto my_data = x;
    (void)my_data;
    return 0;
}
