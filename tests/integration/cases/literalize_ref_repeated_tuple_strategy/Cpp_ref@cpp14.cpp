#include <initializer_list>
#include <string>
#include <vector>
#include <tuple>
int main() {
auto shared = std::make_tuple(
    1,
    "x"
);
auto my_data = std::vector<std::tuple<int, std::string>>{
    shared,
    shared,
};
    (void)my_data;
    return 0;
}
