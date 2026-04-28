#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
struct mgrType_ { void op(auto...) const {} };
struct appType_ { mgrType_ mgr; };
const appType_ app;
auto main() -> int {
app.mgr.op(std::map<std::string, std::variant<std::string, bool>>{{"type", "create"}, {"pr_id", "pr_1"}, {"draft", true}});
app.mgr.op(std::map<std::string, std::variant<std::string, bool>>{{"type", "create"}, {"pr_id", "pr_2"}});
    return 0;
}
