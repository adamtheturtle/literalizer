#include <initializer_list>
#include <string>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
struct clientType_ { void post(auto...) const {} };
struct apiType_ { clientType_ client; };
struct objType_ { apiType_ api; };
const objType_ obj;
void check_() {
obj.api.client.post("hello");
obj.api.client.post(42);
obj.api.client.post(true);
}
