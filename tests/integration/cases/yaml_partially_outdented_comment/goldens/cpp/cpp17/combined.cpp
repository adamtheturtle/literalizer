#include <map>
#include <string>
#include <variant>
#include <vector>
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
my_data = std::map<std::string, std::variant<std::map<std::string, std::variant<std::vector<int>, int>>, int>>{
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
