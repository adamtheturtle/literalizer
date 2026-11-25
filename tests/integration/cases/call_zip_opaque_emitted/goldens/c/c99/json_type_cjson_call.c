#include <cjson/cJSON.h>
static cJSON * process(cJSON *_a0) { (void)_a0; return NULL; }
static void emit(cJSON *_a0, cJSON *_a1) { (void)_a0, (void)_a1; }
int main(void) {
emit(process(cJSON_CreateNumber((double)1)), cJSON_CreateString("2024-01-15T12:00:00Z"));
    return 0;
}
