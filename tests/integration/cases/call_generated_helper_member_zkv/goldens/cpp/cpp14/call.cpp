struct objType_ { template <typename... Args> void ZKV(Args...) const {} };
const objType_ obj;
int main() {
obj.ZKV(1);
    return 0;
}
