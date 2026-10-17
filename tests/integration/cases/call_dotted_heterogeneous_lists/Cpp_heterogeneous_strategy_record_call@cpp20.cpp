#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
struct clientType_ { void go(auto...) const {} };
struct appType_ { clientType_ client; };
const appType_ app;
int main() {
app.client.go(std::vector<int>{1}, std::vector<std::string>{"text"});
    return 0;
}
