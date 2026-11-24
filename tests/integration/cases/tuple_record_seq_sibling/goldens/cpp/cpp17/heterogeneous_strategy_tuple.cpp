#include <map>
#include <string>
#include <tuple>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::variant<std::vector<int>, std::tuple<int, std::string, std::string, int>>>{
    {"scores", std::vector<int>{10, 20, 30}},
    {"args", std::make_tuple(1, "email", "a@gmail.com", 100)},
};
    (void)my_data;
    return 0;
}
