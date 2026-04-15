#include <initializer_list>
#include <string>
#include <vector>
void check_() {
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
