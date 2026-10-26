#include <string>
#include <vector>
struct clientType_ { template <typename... Args> void go(Args...) const {} };
struct appType_ { clientType_ client; };
const appType_ app;
int main() {
app.client.go(std::vector<int>{1}, std::vector<std::string>{"text"});
    return 0;
}
