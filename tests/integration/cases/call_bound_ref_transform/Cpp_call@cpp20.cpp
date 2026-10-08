#include <initializer_list>
#include <vector>
auto f(auto...) { return 0; }
int main() {
auto x = 1;
f(x);
    return 0;
}
