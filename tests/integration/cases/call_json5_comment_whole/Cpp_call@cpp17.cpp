#include <initializer_list>
template <typename... Args> auto f(Args...) { return 0; }
int main() {
// scalar heading
// second heading line
// scalar inline
// inline continuation
// scalar trailing
f(42);
    return 0;
}
