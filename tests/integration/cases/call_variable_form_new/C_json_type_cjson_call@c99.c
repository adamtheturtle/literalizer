#include <cjson/cJSON.h>
static cJSON * make_widget(cJSON *_a0) { (void)_a0; return NULL; }
int main(void) {
CVal my_data = make_widget(cJSON_CreateNumber((double)42));
    (void)my_data;
    return 0;
}
