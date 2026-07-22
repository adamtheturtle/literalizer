#include <initializer_list>
#include <string>
#include <vector>
#include <tuple>
int main() {
auto my_data = std::make_tuple(
    42,
    3.14,
    true,
    false,
    "hello \"world\""
);
    (void)my_data;
    return 0;
}
