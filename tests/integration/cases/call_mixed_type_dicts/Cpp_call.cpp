#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
struct mType_ { auto Op(auto...) const { return 0; } };
const mType_ m;
void check_() {
m.Op(std::map<std::string, std::variant<std::string, bool>>{{"type", "create"}, {"pr_id", "pr_1"}, {"draft", true}});
m.Op(std::map<std::string, std::variant<std::string, bool>>{{"type", "create"}, {"pr_id", "pr_2"}});
}
