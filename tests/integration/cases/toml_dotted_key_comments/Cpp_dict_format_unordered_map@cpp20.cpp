#include <string>
#include <unordered_map>
int main() {
auto my_data = std::unordered_map<std::string, std::unordered_map<std::string, int>>{
    // first dotted key
    // second dotted key
    {"a", std::unordered_map<std::string, int>{{"b", 1}, {"c", 2}}},
};
    (void)my_data;
    return 0;
}
