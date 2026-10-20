#include <initializer_list>
int main() {
auto first = 42;
auto&& my_data = first;
(void)my_data;
my_data = first;
    (void)my_data;
    return 0;
}
