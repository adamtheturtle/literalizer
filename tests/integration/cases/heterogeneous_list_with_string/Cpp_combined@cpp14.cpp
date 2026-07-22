#include <initializer_list>
#include <string>
#include <vector>
#include <tuple>
int main() {
auto my_data = std::make_tuple(
    "hello",
    42
);
(void)my_data;
my_data = std::make_tuple(
    "hello",
    42
);
    (void)my_data;
    return 0;
}
