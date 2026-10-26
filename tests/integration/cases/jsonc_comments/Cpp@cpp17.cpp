#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, int>>{
    // A JSONC input case with both comment forms.
    {"url", "https://example.org/a/*b*/"},  // detail
    // continued
    {"count", 2},  // trailing line comment
};
    (void)my_data;
    return 0;
}
