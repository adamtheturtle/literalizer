#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::map<std::string, std::map<std::string, std::map<std::string, std::string>>>>{
    {"a", std::map<std::string, std::map<std::string, std::map<std::string, std::string>>>{{"b", std::map<std::string, std::map<std::string, std::string>>{{"c", std::map<std::string, std::string>{{"$ref", "deep"}}}}}}},
};
(void)my_data;
my_data = std::map<std::string, std::map<std::string, std::map<std::string, std::map<std::string, std::string>>>>{
    {"a", std::map<std::string, std::map<std::string, std::map<std::string, std::string>>>{{"b", std::map<std::string, std::map<std::string, std::string>>{{"c", std::map<std::string, std::string>{{"$ref", "deep"}}}}}}},
};
    (void)my_data;
    return 0;
}
