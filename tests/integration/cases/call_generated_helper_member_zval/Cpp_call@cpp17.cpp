#include <initializer_list>
struct objType_ { template <typename... Args> void ZVal(Args...) const {} };
const objType_ obj;
int main() {
obj.ZVal(1);
    return 0;
}
