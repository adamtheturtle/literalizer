#include <initializer_list>
#include <string>
int main() {
auto my_data = std::string{""} + '\0' + "x";
    (void)my_data;
    return 0;
}
