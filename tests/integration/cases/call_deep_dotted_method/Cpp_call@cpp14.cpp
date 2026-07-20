#include <initializer_list>
#include <string>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T&&) {} };
struct clientType_ { template <typename... Args> void post(Args...) const {} };
struct apiType_ { clientType_ client; };
struct objType_ { apiType_ api; };
const objType_ obj;
int main() {
obj.api.client.post("hello");
obj.api.client.post(42);
obj.api.client.post(true);
    return 0;
}
