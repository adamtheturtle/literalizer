#include <initializer_list>
#include <vector>
int main() {
auto whole = std::vector<int>{
    1,
    2,
};
auto my_data = std::move(whole);
    (void)my_data;
    return 0;
}
