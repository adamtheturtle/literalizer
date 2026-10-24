#include <initializer_list>
#include <vector>
template <typename... Args> auto DoThing(Args...) { return 0; }
int main() {
DoThing(1);
DoThing(2);
    return 0;
}
