#include <string>
#include <unordered_map>
int main() {
auto my_data = std::unordered_map<std::string, std::unordered_map<std::string, int>>{
    {"section", std::unordered_map<std::string, int>{{"value", 1}}},
};
    (void)my_data;
    return 0;
}
