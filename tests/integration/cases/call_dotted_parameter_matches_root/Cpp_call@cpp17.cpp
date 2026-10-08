#include <initializer_list>
#include <vector>
struct outerType_ { template <typename... Args> void inner(Args...) const {} };
const outerType_ outer;
int main() {
outer.inner(1, 2);
    return 0;
}
