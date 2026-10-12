#include <initializer_list>
#include <vector>
#include <utility>
int main() {
auto shared = std::vector<int>{
    1,
    2,
};
auto&& my_data = shared;
(void)my_data;
my_data = shared;
    (void)my_data;
    return 0;
}
