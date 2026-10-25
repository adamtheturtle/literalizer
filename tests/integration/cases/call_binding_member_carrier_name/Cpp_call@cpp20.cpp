#include <initializer_list>
struct objType_ { [[nodiscard]] auto ZVal(auto...) const { return 0; } };
const objType_ obj;
int main() {
auto my_data = obj.ZVal(42); // note
    (void)my_data;
    return 0;
}
