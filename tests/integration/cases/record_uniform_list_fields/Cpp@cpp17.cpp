#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::vector<std::map<std::string, std::vector<int>>>{
    std::map<std::string, std::vector<int>>{{"scores", std::vector<int>{1, 2}}},
    std::map<std::string, std::vector<int>>{{"scores", std::vector<int>{3, 4}}},
};
    (void)my_data;
    return 0;
}
