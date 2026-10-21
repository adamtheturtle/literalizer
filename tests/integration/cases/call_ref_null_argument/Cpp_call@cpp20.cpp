#include <initializer_list>
#include <cstddef>
auto consume(auto...) { return 0; }
int main() {
auto value = nullptr;
consume(value);
    return 0;
}
