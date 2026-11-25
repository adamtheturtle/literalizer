#include <vector>
struct FooType_ { template <typename... Args> [[nodiscard]] auto bar(Args...) const { return 0; } };
struct fooType_ { FooType_ Foo; };
struct aType_ { fooType_ foo; };
const aType_ a;
int main() {
auto my_data = a.foo.Foo.bar(std::vector<int>{1});
    (void)my_data;
    return 0;
}
