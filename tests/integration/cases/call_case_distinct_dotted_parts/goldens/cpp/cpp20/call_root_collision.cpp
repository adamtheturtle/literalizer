#include <vector>
struct FooType_ { void bar(auto...) const {} };
struct fooType_ { FooType_ Foo; };
const fooType_ foo;
int main() {
foo.Foo.bar(std::vector<int>{1});
    return 0;
}
