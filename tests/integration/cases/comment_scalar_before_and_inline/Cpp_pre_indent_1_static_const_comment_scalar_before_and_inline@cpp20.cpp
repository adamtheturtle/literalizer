#include <initializer_list>
#include <string>
int main() {
    // inline
    static const auto* my_data = // before
    "plain";
    (void)my_data;
    return 0;
}
