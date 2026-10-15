#include <initializer_list>
#include <cstddef>
auto consume(auto...) { return 0; }
int main() {
auto item = nullptr;
consume(item);
    return 0;
}
