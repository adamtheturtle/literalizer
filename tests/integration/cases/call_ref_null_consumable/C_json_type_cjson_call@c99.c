#include <cjson/cJSON.h>
static void consume(cJSON *_a0) { (void)_a0; }
int main(void) {
cJSON *_n0 = cJSON_CreateNull();
cJSON *my_null = _n0;
cJSON *_n0 = cJSON_CreateNull();
cJSON *regular_null = _n0;
consume(my_null);
consume(regular_null);
    return 0;
}
