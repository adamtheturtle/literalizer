#include <initializer_list>
auto consume(auto...) { return 0; }
int main() {
auto shared = 42;
consume(shared);
    return 0;
}
