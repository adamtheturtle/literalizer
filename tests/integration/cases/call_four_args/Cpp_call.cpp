#include <initializer_list>
#include <vector>
auto process(auto...) { return 0; }
int main() {
process(1, 2, 3, 4);
process(10, 20, 30, 40);
    return 0;
}
