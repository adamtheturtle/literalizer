#include <initializer_list>
#include <vector>
auto process(auto...) { return 0; }
int main() {
process(1, 2, 3, 4);
process(5, 6, 7, 8);
    return 0;
}
