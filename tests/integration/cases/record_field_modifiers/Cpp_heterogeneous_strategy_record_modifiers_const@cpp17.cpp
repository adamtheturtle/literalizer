#include <initializer_list>
#include <string>
struct Record0 { int one{}; };
int main() {
const auto my_data = Record0{
    1,
};
    (void)my_data;
    return 0;
}
