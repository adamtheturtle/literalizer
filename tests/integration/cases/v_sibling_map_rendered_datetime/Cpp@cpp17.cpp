#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, std::map<std::string, std::string>>{
    {"a", std::map<std::string, std::string>{{"k", "2020-01-01T00:00:00+00:00"}}},
    {"b", std::map<std::string, std::string>{{"k", "string"}}},
};
    (void)my_data;
    return 0;
}
