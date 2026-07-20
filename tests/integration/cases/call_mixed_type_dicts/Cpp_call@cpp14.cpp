#include <initializer_list>
#include <string>
#include <map>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
struct mgrType_ { template <typename... Args> void run(Args...) const {} };
struct appType_ { mgrType_ mgr; };
const appType_ app;
int main() {
app.mgr.run(std::map<std::string, LiteralizerVariant<std::string, bool>>{{"type", "create"}, {"pr_id", "pr_1"}, {"draft", true}});
app.mgr.run(std::map<std::string, LiteralizerVariant<std::string, bool>>{{"type", "create"}, {"pr_id", "pr_2"}});
    return 0;
}
