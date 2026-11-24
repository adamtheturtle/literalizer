#include <map>
#include <string>
#include <variant>
auto process(auto...) { return 0; }
int main() {
process(std::map<std::string, std::variant<int, std::string>>{{"value", 1}});
process(std::map<std::string, std::variant<int, std::string>>{{"value", "hello"}});
    return 0;
}
