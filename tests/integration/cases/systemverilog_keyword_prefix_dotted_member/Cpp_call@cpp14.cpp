#include <initializer_list>
struct thingType_ { template <typename... Args> void first_value(Args...) const {} };
const thingType_ thing;
int main() {
thing.first_value(1);
    return 0;
}
