#include <map>
#include <string>
#include <tuple>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::map<std::string, std::variant<std::tuple<int, std::string>, std::vector<int>>>>{
    std::map<std::string, std::variant<std::tuple<int, std::string>, std::vector<int>>>{
        {"a", std::make_tuple(
            1,
            "x"
        )},
    },
    std::map<std::string, std::variant<std::tuple<int, std::string>, std::vector<int>>>{
        {"a", std::vector<int>{
            2,
            3,
        }},
    },
};
    (void)my_data;
    return 0;
}
