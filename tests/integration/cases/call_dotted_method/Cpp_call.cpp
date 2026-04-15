#include <initializer_list>
#include <string>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
struct clientType_ { void fetch(auto...) const {} };
struct appType_ { clientType_ client; };
const appType_ app;
void check_() {
app.client.fetch("hello");
app.client.fetch(42);
app.client.fetch(true);
}
