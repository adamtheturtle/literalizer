#include <initializer_list>
#include <vector>
int main() {
auto ref_x = 3;
auto my_data = std::vector<int>{
    Value{ref_x},
    Value{1},
    Value{2},
};
    (void)my_data;
    return 0;
}
