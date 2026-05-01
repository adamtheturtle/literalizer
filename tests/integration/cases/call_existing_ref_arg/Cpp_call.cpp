#include <initializer_list>
#include <vector>
#include <cstddef>
auto process(auto...) { return 0; }
int main() {
auto existing = 42;
process(existing);
    return 0;
}
