#include <map>
#include <string>
#include <variant>
struct processType_ { template <typename... Args> void fetch(Args...) const {} };
struct appType_ { processType_ process; };
const appType_ app;
int main() {
app.process.fetch(std::map<std::string, std::variant<std::string, int, bool>>{{"data", "hello"}});
app.process.fetch(std::map<std::string, std::variant<std::string, int, bool>>{{"data", 42}});
app.process.fetch(std::map<std::string, std::variant<std::string, int, bool>>{{"data", true}});
    return 0;
}
