#include <initializer_list>
#include <string>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
struct clientType_ { template <typename... Args> void fetch(Args...) const {} };
struct appType_ { clientType_ client; };
const appType_ app;
int main() {
app.client.fetch("hello");
app.client.fetch(42);
app.client.fetch(true);
    return 0;
}
