#include <initializer_list>
#include <vector>
auto do_thing(auto...) { return 0; }
int main() {
do_thing(1);
do_thing(2);
    return 0;
}
