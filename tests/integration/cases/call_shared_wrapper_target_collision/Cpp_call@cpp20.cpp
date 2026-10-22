#include <initializer_list>
auto check(auto...) { return 0; }
int main() {
check(42);
    return 0;
}
