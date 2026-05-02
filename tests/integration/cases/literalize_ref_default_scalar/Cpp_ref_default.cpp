#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_var = 1;
auto my_data = std::move(my_var);
    (void)my_data;
    return 0;
}
