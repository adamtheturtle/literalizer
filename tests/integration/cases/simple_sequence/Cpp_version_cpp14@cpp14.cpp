#include <initializer_list>
#include <string>
#include <cstddef>
#include <vector>
#include <tuple>
int main() {
auto my_data = std::make_tuple(
    1,
    "hello",
    true,
    nullptr
);
    (void)my_data;
    return 0;
}
