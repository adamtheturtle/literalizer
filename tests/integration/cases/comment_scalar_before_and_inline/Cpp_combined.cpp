#include <initializer_list>
#include <string>
int main() {
// inline
auto my_data = // before
"plain";
(void)my_data;
// inline
my_data = // before
"plain";
    (void)my_data;
    return 0;
}
