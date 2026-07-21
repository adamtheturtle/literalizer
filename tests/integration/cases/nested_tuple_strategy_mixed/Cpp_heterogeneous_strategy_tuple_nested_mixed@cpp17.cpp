#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
#include <tuple>
int main() {
auto my_data = std::vector<std::variant<std::vector<std::tuple<int, std::string>>, std::vector<std::tuple<std::string, int>>>>{
    std::vector<std::tuple<int, std::string>>{std::make_tuple(1, "Mainframe1")},
    std::vector<std::tuple<std::string, int>>{std::make_tuple("Mainframe2", 2)},
};
    (void)my_data;
    return 0;
}
