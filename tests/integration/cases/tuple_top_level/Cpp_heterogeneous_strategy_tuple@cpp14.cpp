#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
#include <tuple>
int main() {
auto my_data = std::make_tuple(
    1,
    "email",
    "a@gmail.com",
    100
);
    (void)my_data;
    return 0;
}
