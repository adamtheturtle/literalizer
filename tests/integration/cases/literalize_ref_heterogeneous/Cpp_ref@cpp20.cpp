#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<int, std::string>>{
    {"a", 1},
    {"b", "hello"},
};
    (void)my_data;
    return 0;
}
