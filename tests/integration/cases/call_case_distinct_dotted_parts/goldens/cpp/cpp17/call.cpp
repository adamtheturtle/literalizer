#include <vector>
struct FooType_ { template <typename... Args> void bar(Args...) const {} };
struct fooType_ { FooType_ Foo; };
struct aType_ { fooType_ foo; };
const aType_ a;
int main() {
a.foo.Foo.bar(std::vector<int>{1});
    return 0;
}
