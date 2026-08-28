#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::vector<int>, int, std::string>>{
    {"flow", std::vector<int>{
        1,
        // After the first element.
        2,
    }},
    // Between the key and its value.
    {"gap", 3},
    // On the block scalar header.
    {"block", "Text.\n"},
    {"anchored", 4},
    {"alias", 4},
    // On the alias.
};
    (void)my_data;
    return 0;
}
