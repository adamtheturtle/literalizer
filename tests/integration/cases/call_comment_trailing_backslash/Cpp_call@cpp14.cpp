#include <initializer_list>
#include <vector>
template <typename... Args> auto process(Args...) { return 0; }
int main() {
process(1);  // trail \ .
process(2);  // second
    return 0;
}
