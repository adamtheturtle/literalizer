#include <initializer_list>
#include <string>
struct Record0 { int a{}; };
int main() {
auto ZVal = Record0{
    .a = 1,
};
    (void)ZVal;
    return 0;
}
