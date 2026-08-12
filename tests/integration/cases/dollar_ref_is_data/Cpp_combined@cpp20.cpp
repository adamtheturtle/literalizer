#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::map<std::string, std::string>>{
    {"value", std::map<std::string, std::string>{{"$ref", "foo"}}},
};
(void)my_data;
my_data = std::map<std::string, std::map<std::string, std::string>>{
    {"value", std::map<std::string, std::string>{{"$ref", "foo"}}},
};
    (void)my_data;
    return 0;
}
