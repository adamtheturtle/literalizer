#include <initializer_list>
#include <vector>
#include <tuple>
int main() {
auto my_data = std::make_tuple(
    1,
    2.5,
    3
);
    (void)my_data;
    return 0;
}
