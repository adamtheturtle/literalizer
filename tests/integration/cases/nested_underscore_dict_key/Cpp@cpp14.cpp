#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<std::map<std::string, int>>>{
    {"outer", std::vector<std::map<std::string, int>>{std::map<std::string, int>{{"_", 1}}}},
};
    (void)my_data;
    return 0;
}
