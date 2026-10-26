#include <map>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::vector<std::map<std::string, int>>>{
    std::vector<std::map<std::string, int>>{std::map<std::string, int>{{"a", 1}}},
    std::vector<std::map<std::string, int>>{std::map<std::string, int>{{"a", 2}}},
};
    (void)my_data;
    return 0;
}
