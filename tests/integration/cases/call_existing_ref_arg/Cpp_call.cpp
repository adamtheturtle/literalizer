#include <initializer_list>
#include <vector>
#include <cstddef>
#include <variant>
auto send(auto...) { return 0; }
int main() {
auto existing = 42;
send(existing);
    return 0;
}
