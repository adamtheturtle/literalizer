#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_arena_n0 = cJSON_CreateObject();
cJSON *literalizer_arena_n1 = cJSON_CreateNumber((double)1);
cJSON_AddItemToObject(literalizer_arena_n0, "a", literalizer_arena_n1);
cJSON *arena = literalizer_arena_n0;
    (void)arena;
    return 0;
}
