#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
#include <variant>
struct workerType_ { template <typename... Args> void process(Args...) const {} };
struct apiType_ { workerType_ worker; };
const apiType_ api;
int main() {
api.worker.process(std::vector<std::variant<int, std::map<std::string, std::nullptr_t>>>{1, std::map<std::string, std::nullptr_t>{}}, 42);
api.worker.process(std::vector<std::variant<int, std::map<std::string, std::string>>>{2, std::map<std::string, std::string>{{"x", "s"}}}, 43);
    return 0;
}
