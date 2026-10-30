#include <vector>
struct FooType_ { template <typename... Args> void bar(Args...) const {} };
struct fooType_ { FooType_ Foo; };
const fooType_ foo;
int main() {
foo.Foo.bar(std::vector<int>{1});
    return 0;
}
