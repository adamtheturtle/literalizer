#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<std::map<std::string, std::vector<int>>>>{
    {"a", std::vector<std::map<std::string, std::vector<int>>>{std::map<std::string, std::vector<int>>{{"item", std::vector<int>{1}}}}},
    {"b", std::vector<std::map<std::string, std::vector<int>>>{std::map<std::string, std::vector<int>>{{"item", std::vector<int>{2}}}}},
};
    (void)my_data;
    return 0;
}
