#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::map<std::string, std::variant<std::string, int>>>{
    std::map<std::string, std::variant<std::string, int>>{{"k", "2040-01-01T00:00:00+00:00"}},
    std::map<std::string, std::variant<std::string, int>>{{"k", 1}},
};
    (void)my_data;
    return 0;
}
