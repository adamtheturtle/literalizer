#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<std::vector<int>>>{
    {"a", std::vector<std::vector<int>>{std::vector<int>{1, 2}}},
    {"b", std::vector<std::vector<int>>{std::vector<int>{3}}},
};
    (void)my_data;
    return 0;
}
