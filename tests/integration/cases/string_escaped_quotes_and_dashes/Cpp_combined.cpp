#include <initializer_list>
#include <string>
int main() {
std::string my_data = "hello \"world\" -- not a comment";
(void)my_data;
my_data = "hello \"world\" -- not a comment";
    (void)my_data;
    return 0;
}
