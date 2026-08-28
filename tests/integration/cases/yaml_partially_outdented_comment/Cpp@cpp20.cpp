#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::map<std::string, std::variant<std::vector<int>, int>>, int>>{
    {"a", std::map<std::string, std::variant<std::vector<int>, int>>{
        {"b", std::vector<int>{1}},
        // Outdented from the sequence, so the inner mapping claims this.
        {"c", 2},
    }},
    // Outdented from the inner mapping too, so the root claims this.
    {"d", 3},
};
    (void)my_data;
    return 0;
}
