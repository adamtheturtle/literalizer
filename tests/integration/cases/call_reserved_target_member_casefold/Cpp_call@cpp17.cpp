struct objType_ { template <typename... Args> void BEGIN(Args...) const {} };
const objType_ obj;
int main() {
obj.BEGIN(42);
    return 0;
}
