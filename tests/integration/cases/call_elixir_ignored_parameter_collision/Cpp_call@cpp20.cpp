#include <initializer_list>
#include <vector>
auto f(auto...) { return 0; }
int main() {
f(1, 2);
    return 0;
}
