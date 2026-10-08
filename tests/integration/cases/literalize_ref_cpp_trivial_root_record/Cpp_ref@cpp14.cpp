#include <initializer_list>
#include <string>
struct Record1 { int value{}; };
struct Record0 { Record1 child; };
int main() {
auto first = Record0{
    {
        1,
    },
};
auto my_data = first;
    (void)my_data;
    return 0;
}
