#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::map<std::string, int>>{
    {"first", std::map<std::string, int>{{"x", 1}, {"y", 2}}},
    {"second", std::map<std::string, int>{{"z", 3}}},
};
    (void)my_data;
    return 0;
}
