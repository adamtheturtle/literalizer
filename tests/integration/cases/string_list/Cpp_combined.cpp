#include <string>
#include <vector>
void _check() {
auto my_data = std::vector<std::string>{
    "foo",
    "bar",
    "baz",
};
my_data = std::vector<std::string>{
    "foo",
    "bar",
    "baz",
};
}
