#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::map<std::string, std::variant<long long, int>>>{
    std::map<std::string, std::variant<long long, int>>{{"k", 2208988800}},
    std::map<std::string, std::variant<long long, int>>{{"k", 1}},
};
    (void)my_data;
    return 0;
}
