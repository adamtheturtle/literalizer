#include <initializer_list>
#include <vector>
int main() {
auto my_data = std::vector<std::vector<std::vector<int>>>{
    std::vector<std::vector<int>>{std::vector<int>{1}},
};
    (void)my_data;
    return 0;
}
