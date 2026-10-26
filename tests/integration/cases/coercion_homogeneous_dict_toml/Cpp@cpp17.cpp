#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, std::map<std::string, int>>{
    {"_", std::map<std::string, int>{{"a", 1}, {"b", 2}}},
};
    (void)my_data;
    return 0;
}
