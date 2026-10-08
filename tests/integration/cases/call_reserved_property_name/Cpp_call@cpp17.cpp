#include <initializer_list>
#include <vector>
struct fooType_ { template <typename... Args> void class(Args...) const {} };
const fooType_ foo;
int main() {
foo.class(1);
    return 0;
}
