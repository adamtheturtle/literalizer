#include <initializer_list>
#include <vector>
auto f(auto...) { return 0; }
int main() {
// selected heading
f(1, 2);  // selected inline
    return 0;
}
