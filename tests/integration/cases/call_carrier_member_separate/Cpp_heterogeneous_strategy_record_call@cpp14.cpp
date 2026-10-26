#include <string>
#include <vector>
struct appType_ { template <typename... Args> void go(Args...) const {} };
const appType_ app;
int main() {
app.go(std::vector<int>{1}, std::vector<std::string>{"text"});
    return 0;
}
