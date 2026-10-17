#include <initializer_list>
#include <vector>
struct clientType_ { void go(auto...) const {} };
struct appType_ { clientType_ client; };
const appType_ app;
int main() {
app.client.go(std::vector<int>{1}, std::vector<int>{2});
    return 0;
}
