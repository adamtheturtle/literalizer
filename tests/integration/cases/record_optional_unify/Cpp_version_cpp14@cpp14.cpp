#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<std::map<std::string, int>>>{
    {"items", std::vector<std::map<std::string, int>>{std::map<std::string, int>{{"id", 1}}, std::map<std::string, int>{{"id", 2}, {"count", 10}}, std::map<std::string, int>{{"id", 3}, {"count", 20}}}},
};
    (void)my_data;
    return 0;
}
