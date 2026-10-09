#include <initializer_list>
#include <string>
struct Record0 { int x{}; };
#include <utility>
int main() {
auto ref_data = Record0{
    1,
};
static auto my_data = ref_data;
    (void)my_data;
    return 0;
}
