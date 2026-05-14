#include <initializer_list>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::string>{
    "foo",
    "bar",
    "baz",
};
    (void)my_data;
    return 0;
}
