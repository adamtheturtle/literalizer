#include <initializer_list>
#include <string>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
struct clientType_ { auto send(auto...) const { return 0; } };
struct nsType_ { clientType_ client; };
const nsType_ ns;
void check_() {
ns.client.send("hello");
ns.client.send(42);
ns.client.send(true);
}
