#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<std::vector<std::vector<std::vector<int>>>>>{
    {"deep", std::vector<std::vector<std::vector<std::vector<int>>>>{std::vector<std::vector<std::vector<int>>>{std::vector<std::vector<int>>{std::vector<int>{1}}}}},
};
(void)my_data;
my_data = std::map<std::string, std::vector<std::vector<std::vector<std::vector<int>>>>>{
    {"deep", std::vector<std::vector<std::vector<std::vector<int>>>>{std::vector<std::vector<std::vector<int>>>{std::vector<std::vector<int>>{std::vector<int>{1}}}}},
};
    (void)my_data;
    return 0;
}
