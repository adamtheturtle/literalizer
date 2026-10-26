#include <vector>
struct appType_ { template <typename... Args> void go(Args...) const {} };
const appType_ app;
int main() {
app.go(std::vector<int>{1}, std::vector<int>{2});
    return 0;
}
