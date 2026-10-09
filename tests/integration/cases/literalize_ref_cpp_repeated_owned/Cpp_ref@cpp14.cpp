#include <initializer_list>
#include <vector>
int main() {
auto shared = std::vector<int>{
    1,
    2,
};
auto my_data = std::vector<std::vector<int>>{
    shared,
    shared,
};
    (void)my_data;
    return 0;
}
