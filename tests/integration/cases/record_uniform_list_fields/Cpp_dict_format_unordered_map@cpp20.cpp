#include <initializer_list>
#include <string>
#include <unordered_map>
#include <vector>
int main() {
auto my_data = std::vector<std::unordered_map<std::string, std::vector<int>>>{
    std::unordered_map<std::string, std::vector<int>>{{"scores", std::vector<int>{1, 2}}},
    std::unordered_map<std::string, std::vector<int>>{{"scores", std::vector<int>{3, 4}}},
};
    (void)my_data;
    return 0;
}
