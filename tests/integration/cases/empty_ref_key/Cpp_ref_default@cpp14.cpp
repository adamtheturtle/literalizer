#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto external_value = std::map<std::string, std::string>{
    {"_", "_"},
};
auto my_data = std::vector<std::map<std::string, std::string>>{
    std::move(external_value),
};
    (void)my_data;
    return 0;
}
