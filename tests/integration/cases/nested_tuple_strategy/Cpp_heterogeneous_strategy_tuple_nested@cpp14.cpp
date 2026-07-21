#include <initializer_list>
#include <string>
#include <vector>
#include <tuple>
int main() {
auto my_data = std::vector<std::tuple<int, std::string>>{
    std::make_tuple(1, "Mainframe1"),
};
    (void)my_data;
    return 0;
}
