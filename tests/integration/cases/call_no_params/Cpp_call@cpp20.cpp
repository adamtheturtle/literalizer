#include <initializer_list>
#include <vector>
#include <cstddef>
auto process(auto...) { return 0; }
int main() {
process();
process();
    return 0;
}
