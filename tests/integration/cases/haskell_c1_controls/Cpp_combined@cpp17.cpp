#include <initializer_list>
#include <string>
int main() {
const auto* my_data = "0aF";
(void)my_data;
my_data = "0aF";
    (void)my_data;
    return 0;
}
