#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::map<std::string, int>>{
    {"section", std::map<std::string, int>{{"value", 1}}},
};
    (void)my_data;
    return 0;
}
