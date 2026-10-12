#include <initializer_list>
struct objType_ { void ZKV(auto...) const {} };
const objType_ obj;
int main() {
obj.ZKV(1);
    return 0;
}
