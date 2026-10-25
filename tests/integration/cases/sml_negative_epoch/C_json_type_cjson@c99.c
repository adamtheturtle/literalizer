#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateArray();
cJSON *_n1 = cJSON_CreateString("1960-01-01T00:00:00+00:00");
cJSON_AddItemToArray(_n0, _n1);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
