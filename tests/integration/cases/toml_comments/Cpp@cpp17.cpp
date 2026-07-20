#include <initializer_list>
#include <string>
#include <map>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<int, std::string>>{
    // before
    {"answer", 42},  // inline
    {"plain", "ok"},
    // trailing
};
    (void)my_data;
    return 0;
}
