#include <initializer_list>
#include <string>
#include <map>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, int>>{
    {"url", "https://example.org/a/*b*/"},
    {"count", 2},
};
    (void)my_data;
    return 0;
}
