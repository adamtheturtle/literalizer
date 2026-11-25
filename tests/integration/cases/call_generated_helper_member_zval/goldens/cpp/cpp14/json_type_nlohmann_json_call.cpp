#include <nlohmann/json.hpp>
struct objType_ { template <typename... Args> void ZVal(Args...) const {} };
const objType_ obj;
int main() {
    try {
obj.ZVal(nlohmann::json(1));
        return 0;
    } catch (...) {
        return 1;
    }
}
