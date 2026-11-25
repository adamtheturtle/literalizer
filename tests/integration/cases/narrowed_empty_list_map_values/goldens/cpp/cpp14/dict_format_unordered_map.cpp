#include <string>
#include <unordered_map>
#include <vector>
int main() {
auto my_data = std::unordered_map<std::string, std::vector<int>>{
    {"a", std::vector<int>{1}},
    {"b", std::vector<int>{}},
};
    (void)my_data;
    return 0;
}
