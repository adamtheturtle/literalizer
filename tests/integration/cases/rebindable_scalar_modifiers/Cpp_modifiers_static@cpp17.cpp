#include <initializer_list>
int main() {
    static auto my_data = 1;
(void)my_data;
    my_data = 1;
    (void)my_data;
    return 0;
}
