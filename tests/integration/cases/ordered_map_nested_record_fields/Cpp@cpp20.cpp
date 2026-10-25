#include <initializer_list>
#include <string>
#include <map>
#include <utility>
#include <vector>
int main() {
auto my_data = std::vector<std::pair<std::string, std::map<std::string, int>>>{
    {"first", std::map<std::string, int>{{"x", 1}}},
    {"second", std::map<std::string, int>{{"y", 2}}},
};
    (void)my_data;
    return 0;
}
