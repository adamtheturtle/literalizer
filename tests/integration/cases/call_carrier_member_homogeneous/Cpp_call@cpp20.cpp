#include <initializer_list>
#include <vector>
struct appType_ { void go(auto...) const {} };
const appType_ app;
int main() {
app.go(std::vector<int>{1}, std::vector<int>{2});
    return 0;
}
