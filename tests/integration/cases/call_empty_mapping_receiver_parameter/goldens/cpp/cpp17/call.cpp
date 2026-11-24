#include <cstddef>
#include <map>
#include <string>
struct apiType_ { template <typename... Args> void process(Args...) const {} };
const apiType_ api;
int main() {
api.process(std::map<std::string, std::nullptr_t>{});
    return 0;
}
