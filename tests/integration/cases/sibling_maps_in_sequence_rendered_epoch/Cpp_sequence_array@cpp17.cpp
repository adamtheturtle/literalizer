#include <initializer_list>
#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = {
    std::map<std::string, std::variant<std::string, int>>{{"k", "2040-01-01T00:00:00+00:00"}},
    std::map<std::string, std::variant<std::string, int>>{{"k", 1}},
};
    (void)my_data;
    return 0;
}
