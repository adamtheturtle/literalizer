#include <string>
#include <tuple>
#include <vector>
int main() {
auto my_data = std::vector<std::tuple<int, std::string>>{
    std::make_tuple(1, "a"),
    std::make_tuple(2, "b"),
};
    (void)my_data;
    return 0;
}
