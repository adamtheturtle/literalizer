#include <cjson/cJSON.h>
static void process(cJSON *_a0) { (void)_a0; }
int main(void) {
cJSON *literalizer_arena_n0 = cJSON_CreateObject();
cJSON *literalizer_arena_n1 = cJSON_CreateNumber((double)1);
cJSON_AddItemToObject(literalizer_arena_n0, "a", literalizer_arena_n1);
cJSON *arena = literalizer_arena_n0;
cJSON *literalizer_ZVal_n2 = cJSON_CreateObject();
cJSON *literalizer_ZVal_n3 = cJSON_CreateNumber((double)1);
cJSON_AddItemToObject(literalizer_ZVal_n2, "a", literalizer_ZVal_n3);
cJSON *ZVal = literalizer_ZVal_n2;
cJSON *literalizer_ZKV_n4 = cJSON_CreateObject();
cJSON *literalizer_ZKV_n5 = cJSON_CreateNumber((double)1);
cJSON_AddItemToObject(literalizer_ZKV_n4, "a", literalizer_ZKV_n5);
cJSON *ZKV = literalizer_ZKV_n4;
process(arena);
process(ZVal);
process(ZKV);
    return 0;
}
