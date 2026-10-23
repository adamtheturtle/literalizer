#include <cjson/cJSON.h>
static void obj_std_stub_(cJSON *_a0) { (void)_a0; }
struct objType_ { void (*std)(cJSON *); };
static const struct objType_ obj = { .std = obj_std_stub_ };
int main(void) {
obj.std(cJSON_CreateNumber((double)1));
    return 0;
}
