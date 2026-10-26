#include <vector>
#include <utility>
#include <map>
#include <string>
#include <variant>
int main() {
            auto shared = std::vector<int>{
                1,
                2,
            };
            auto other = 3;
            const auto* payload = "\n    shared : Val\nshared = RInt 99";
            auto my_data = std::map<std::string, std::variant<std::vector<int>, int, std::string>>{
                {"a", std::move(shared)},
                {"b", other},
                {"payload", payload},
            };
    (void)my_data;
    return 0;
}
