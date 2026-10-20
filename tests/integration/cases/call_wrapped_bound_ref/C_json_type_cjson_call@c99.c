#include <cjson/cJSON.h>
static void make_widget(cJSON *_a0) { (void)_a0; }
int main(void) {
cJSON *_n0 = cJSON_CreateNumber((double)1);
cJSON *value = _n0;
make_widget(value);
    return 0;
}
