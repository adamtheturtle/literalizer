#include <initializer_list>
#include <string>
#include <vector>
#include <map>
#include <variant>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
auto big_list = std::vector<std::string>{
    "x",
};
process(std::map<std::string, std::vector<std::string>>{{"k", std::move(big_list)}}, 2);
    return 0;
}
