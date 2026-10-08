#include <initializer_list>
#include <vector>
auto DoThing(auto...) { return 0; }
int main() {
DoThing(1);
DoThing(2);
    return 0;
}
