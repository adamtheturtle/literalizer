#include <initializer_list>
#include <string>
int main() {
const auto* my_data = "";
(void)my_data;
my_data = "";
    (void)my_data;
    return 0;
}
