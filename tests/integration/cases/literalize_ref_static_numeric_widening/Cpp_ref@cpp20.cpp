#include <initializer_list>
int main() {
auto seed = 1;
static auto my_data = seed;
    (void)my_data;
    return 0;
}
