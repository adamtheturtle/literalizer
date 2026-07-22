#include <initializer_list>
#include <string>
#include <vector>
#include <tuple>
int main() {
auto my_data = std::make_tuple(
    1,
    "hello"
);
    (void)my_data;
    return 0;
}
