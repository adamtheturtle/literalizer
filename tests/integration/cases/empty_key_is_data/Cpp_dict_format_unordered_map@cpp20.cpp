#include <initializer_list>
#include <string>
#include <unordered_map>
#include <vector>
int main() {
auto my_data = std::vector<std::unordered_map<std::string, std::string>>{
    std::unordered_map<std::string, std::string>{{"", "external_value"}},
};
    (void)my_data;
    return 0;
}
