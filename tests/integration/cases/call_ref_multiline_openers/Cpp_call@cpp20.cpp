#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
auto consume(auto...) { return 0; }
int main() {
auto foo = 42;
consume(std::vector<std::map<std::string, int>>{
    std::map<std::string, std::variant<int, std::string>>{
        {"other", 1},
    },
    foo,
}, std::map<std::string, int>{
    {"left", foo},
    {"other", 1},
});
    return 0;
}
