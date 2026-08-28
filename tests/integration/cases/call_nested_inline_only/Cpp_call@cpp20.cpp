#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
auto f(auto...) { return 0; }
int main() {
f(2, "hello");  // trailing note
f(3, "world");  // another note
    return 0;
}
