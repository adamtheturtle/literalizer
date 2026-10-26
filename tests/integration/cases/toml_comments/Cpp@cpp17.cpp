#include <map>
#include <string>
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
