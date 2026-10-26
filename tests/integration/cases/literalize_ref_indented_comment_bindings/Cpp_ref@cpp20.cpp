#include <vector>
#include <utility>
#include <string>
#include <variant>
int main() {
        auto shared = std::vector<int>{
            1,
            2,
        };
        auto my_data = std::vector<std::variant<std::string, std::vector<int>>>{
            // A leading comment with { braces, "quotes", and // markers
            "first\n{ \"quoted\" // text }",
            std::move(shared),
        };
    (void)my_data;
    return 0;
}
