#include <cjson/cJSON.h>
static void make_widget(cJSON *_a0) { (void)_a0; }
int main(void) {
cJSON *literalizer_value_n0 = cJSON_CreateNumber((double)1);
cJSON *value = literalizer_value_n0;
make_widget(value);
    return 0;
}
