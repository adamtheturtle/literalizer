#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::vector<std::variant<std::map<std::string, std::string>, std::string>>>{
    std::vector<std::variant<std::map<std::string, std::string>, std::string>>{
        std::map<std::string, std::string>{{"item", "existing"}},
        "kept",
        // This comment trails the first pair.
    },
    std::vector<std::variant<std::map<std::string, std::string>, std::string>>{std::map<std::string, std::string>{{"item", "next"}}, "also kept"},
    // This comment describes the last pair.
    std::vector<std::variant<std::map<std::string, std::string>, std::string>>{std::map<std::string, std::string>{{"item", "last"}}, "kept too"},
};
    (void)my_data;
    return 0;
}
