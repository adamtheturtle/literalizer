#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::vector<std::vector<std::map<std::string, std::string>>>{
    std::vector<std::map<std::string, std::string>>{std::map<std::string, std::string>{{"$ref", "my_str"}}},
};
(void)my_data;
my_data = std::vector<std::vector<std::map<std::string, std::string>>>{
    std::vector<std::map<std::string, std::string>>{std::map<std::string, std::string>{{"$ref", "my_str"}}},
};
    (void)my_data;
    return 0;
}
