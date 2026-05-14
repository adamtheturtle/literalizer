#include <initializer_list>
#include <string>
#include <map>
int main() {
auto deep = std::map<std::string, std::string>{
    {"_", "_"},
};
auto my_data = std::map<std::string, std::map<std::string, std::map<std::string, std::map<std::string, std::string>>>>{
    {"a", std::map<std::string, std::map<std::string, std::map<std::string, std::string>>>{{"b", std::map<std::string, std::map<std::string, std::string>>{{"c", std::move(deep)}}}}},
};
    (void)my_data;
    return 0;
}
