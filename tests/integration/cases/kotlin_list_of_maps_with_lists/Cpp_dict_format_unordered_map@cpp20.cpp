#include <initializer_list>
#include <string>
#include <unordered_map>
#include <vector>
int main() {
auto my_data = std::vector<std::unordered_map<std::string, std::vector<int>>>{
    std::unordered_map<std::string, std::vector<int>>{{"a", std::vector<int>{1}}},
    std::unordered_map<std::string, std::vector<int>>{{"a", std::vector<int>{2}}},
};
    (void)my_data;
    return 0;
}
