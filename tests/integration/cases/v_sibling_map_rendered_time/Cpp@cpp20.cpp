#include <initializer_list>
#include <string>
#include <map>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::map<std::string, std::string>>{
    {"a", std::map<std::string, std::string>{{"k", "07:30:00"}}},
    {"b", std::map<std::string, std::string>{{"k", "string"}}},
};
    (void)my_data;
    return 0;
}
