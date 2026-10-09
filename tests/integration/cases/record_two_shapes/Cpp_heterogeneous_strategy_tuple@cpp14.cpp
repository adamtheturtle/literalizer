#include <initializer_list>
#include <string>
struct Record1 { int count{}; int rate{}; };
struct Record2 { int retries{}; int timeout{}; };
struct Record0 { Record1 metrics; Record2 flags; };
int main() {
auto my_data = Record0{
    {
        100,
        50,
    },
    {
        3,
        30,
    },
};
    (void)my_data;
    return 0;
}
