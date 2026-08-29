#include <initializer_list>
#include <string>
#include <vector>
#include <utility>
#include <variant>
auto process(auto...) { return 0; }
int main() {
auto big_list = std::vector<std::string>{
    "x",
};
process(std::vector<std::pair<std::string, std::vector<std::string>>>{{"m", std::move(big_list)}});
    return 0;
}
