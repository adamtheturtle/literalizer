#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<std::vector<std::map<std::string, int>>>>{
    {"groups", std::vector<std::vector<std::map<std::string, int>>>{std::vector<std::map<std::string, int>>{std::map<std::string, int>{{"id", 1}}}, std::vector<std::map<std::string, int>>{std::map<std::string, int>{{"id", 2}}}}},
};
(void)my_data;
my_data = std::map<std::string, std::vector<std::vector<std::map<std::string, int>>>>{
    {"groups", std::vector<std::vector<std::map<std::string, int>>>{std::vector<std::map<std::string, int>>{std::map<std::string, int>{{"id", 1}}}, std::vector<std::map<std::string, int>>{std::map<std::string, int>{{"id", 2}}}}},
};
    (void)my_data;
    return 0;
}
