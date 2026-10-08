#include <initializer_list>
#include <vector>
template <typename... Args> auto do_thing(Args...) { return 0; }
int main() {
do_thing(1);
do_thing(2);
    return 0;
}
