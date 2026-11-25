#include <map>
#include <string>
#include <variant>
struct apiType_ { template <typename... Args> void fetch(Args...) const {} };
struct processType_ { apiType_ api; };
const processType_ process;
int main() {
process.api.fetch(std::map<std::string, std::variant<std::string, int, bool>>{{"data", "hello"}});
process.api.fetch(std::map<std::string, std::variant<std::string, int, bool>>{{"data", 42}});
process.api.fetch(std::map<std::string, std::variant<std::string, int, bool>>{{"data", true}});
    return 0;
}
