#include <initializer_list>
#include <string>
#include <map>
#include <variant>
auto send(auto...) { return 0; }
int main() {
send(std::map<std::string, std::variant<int, std::string>>{{"a", 1}, {"b", "x"}});
    return 0;
}
