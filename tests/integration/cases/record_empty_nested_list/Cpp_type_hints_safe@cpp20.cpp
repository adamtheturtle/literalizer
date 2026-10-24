#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
int main() {
auto my_data = std::map<std::string, std::vector<std::vector<int>>>{
    {"a", std::vector<std::vector<int>>{std::vector<int>{1, 2}, std::vector<int>{3}}},
    {"b", std::vector<std::vector<int>>{std::vector<int>{}, std::vector<int>{1}}},
};
    (void)my_data;
    return 0;
}
