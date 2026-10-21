#include <initializer_list>
#include <string>
#include <array>
int main() {
auto my_data = std::array<std::string, 3>{
    "foo",
    "bar",
    "baz",
};
    (void)my_data;
    return 0;
}
