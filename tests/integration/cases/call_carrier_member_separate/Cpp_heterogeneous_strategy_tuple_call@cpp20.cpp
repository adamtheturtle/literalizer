#include <string>
#include <vector>
struct appType_ { void go(auto...) const {} };
const appType_ app;
int main() {
app.go(std::vector<int>{1}, std::vector<std::string>{"text"});
    return 0;
}
