#include <initializer_list>
#include <string>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
struct clientType_ { template <typename... Args> auto fetch(Args...) const { return 0; } };
struct appType_ { clientType_ client; };
const appType_ app;
template <typename... Args> auto emit(Args...) { return 0; }
int main() {
emit(app.client.fetch("hello"));
emit(app.client.fetch(42));
emit(app.client.fetch(true));
    return 0;
}
