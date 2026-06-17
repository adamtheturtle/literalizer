#include <initializer_list>
#include <vector>
auto record(auto...) { return 0; }
auto flush(auto...) { return 0; }
int main() {
record(42);
flush(3);
    return 0;
}
