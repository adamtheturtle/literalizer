#include <initializer_list>
#include <string>
#include <map>
struct Record1 { int count{}; int rate{}; };
struct Record2 { int retries{}; int timeout{}; };
struct Record0 { Record1 metrics; Record2 flags; };
int main() {
auto my_data = Record0{
    .metrics = Record1{
        .count = 100,
        .rate = 50,
    },
    .flags = Record2{
        .retries = 3,
        .timeout = 30,
    },
};
    (void)my_data;
    return 0;
}
