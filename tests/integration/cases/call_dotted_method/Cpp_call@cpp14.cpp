#include <initializer_list>
#include <string>
#include <vector>
#include <tuple>
struct clientType_ { template <typename... Args> void fetch(Args...) const {} };
struct appType_ { clientType_ client; };
const appType_ app;
int main() {
app.client.fetch("hello");
app.client.fetch(42);
app.client.fetch(true);
    return 0;
}
