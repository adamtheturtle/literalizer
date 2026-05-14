#include <initializer_list>
#include <string>
#include <map>
#include <vector>
auto process(auto...) { return 0; }
int main() {
// Test cases
process(std::map<std::string, std::string>{{"type", "create"}, {"pr_id", "pr_1"}});  // first case
process(std::map<std::string, std::string>{{"type", "update"}, {"pr_id", "pr_2"}});  // second case
// third case
process(std::map<std::string, std::string>{{"type", "delete"}, {"pr_id", "pr_3"}});
    return 0;
}
