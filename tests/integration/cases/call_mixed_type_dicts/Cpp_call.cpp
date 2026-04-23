#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
struct mgrType_ { auto Op(auto...) const { return 0; } };
const mgrType_ mgr;
void check_() {
mgr.Op(std::map<std::string, std::variant<std::string, bool>>{{"type", "create"}, {"pr_id", "pr_1"}, {"draft", true}});
mgr.Op(std::map<std::string, std::variant<std::string, bool>>{{"type", "create"}, {"pr_id", "pr_2"}});
}
