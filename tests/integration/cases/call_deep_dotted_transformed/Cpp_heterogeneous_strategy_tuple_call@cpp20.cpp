#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
#include <tuple>
struct clientType_ { [[nodiscard]] auto fetch(auto...) const { return 0; } };
struct appType_ { clientType_ client; };
const appType_ app;
auto emit(auto...) { return 0; }
int main() {
emit(app.client.fetch("hello"));
emit(app.client.fetch(42));
emit(app.client.fetch(true));
    return 0;
}
