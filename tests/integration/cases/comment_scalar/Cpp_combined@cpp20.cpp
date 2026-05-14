#include <initializer_list>
int main() {
auto my_data = // note
42;
(void)my_data;
my_data = // note
42;
    (void)my_data;
    return 0;
}
