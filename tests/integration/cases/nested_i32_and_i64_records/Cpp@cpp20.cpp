#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<std::vector<std::map<std::string, int>>, std::vector<std::map<std::string, long long>>>>{
    std::vector<std::map<std::string, int>>{std::map<std::string, int>{{"value", 1}}},
    std::vector<std::map<std::string, long long>>{std::map<std::string, long long>{{"value", 1099511627776}}},
};
    (void)my_data;
    return 0;
}
