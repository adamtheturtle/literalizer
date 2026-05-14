#include <initializer_list>
#include <vector>
auto process(auto...) { return 0; }
int main() {
process(1, 2);
process(3, 4);
    return 0;
}
