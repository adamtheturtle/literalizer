#include <initializer_list>
#include <vector>
int main() {
auto my_data = std::vector<int>{
    1,
    // closing
};
    (void)my_data;
    return 0;
}
