#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
struct clientType_ { void fetch(auto...) const {} };
struct appType_ { clientType_ client; };
const appType_ app;
int main() {
app.client.fetch("hello");
app.client.fetch(42);
app.client.fetch(true);
    return 0;
}
