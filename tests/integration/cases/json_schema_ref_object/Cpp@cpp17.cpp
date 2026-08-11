#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::map<std::string, std::string>>{
    {"schema", std::map<std::string, std::string>{{"$ref", "#/defs/Foo"}}},
};
    (void)my_data;
    return 0;
}
