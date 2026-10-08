#include <initializer_list>
#include <vector>
struct fooType_ { void class(auto...) const {} };
const fooType_ foo;
int main() {
foo.class(1);
    return 0;
}
