#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
#include <variant>
struct apiType_ { template <typename... Args> void process(Args...) const {} };
const apiType_ api;
int main() {
api.process(std::map<std::string, std::nullptr_t>{});
    return 0;
}
