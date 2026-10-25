#include <initializer_list>
struct thingType_ { template <typename... Args> void Before(Args...) const {} };
const thingType_ thing;
int main() {
thing.Before(1);
    return 0;
}
