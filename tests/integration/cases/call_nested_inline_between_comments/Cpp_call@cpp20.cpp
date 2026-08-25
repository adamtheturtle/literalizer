#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
auto f(auto...) { return 0; }
int main() {
f(2, "hello");  // trailing note
// next element
f(3, "world");
    return 0;
}
