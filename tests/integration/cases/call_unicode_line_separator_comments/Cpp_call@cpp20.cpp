#include <initializer_list>
#include <vector>
auto process(auto...) { return 0; }
int main() {
process(1);  // note<U+2028>still commented<U+2029>done
    return 0;
}
