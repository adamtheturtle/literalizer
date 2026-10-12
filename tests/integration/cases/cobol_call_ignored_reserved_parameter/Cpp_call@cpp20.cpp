#include <initializer_list>
auto process(auto...) { return 0; }
int main() {
process(42);
    return 0;
}
