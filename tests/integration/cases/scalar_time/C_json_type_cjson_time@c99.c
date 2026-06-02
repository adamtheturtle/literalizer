#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateString("09:30:00");
cJSON_AddItemToObject(_n0, "starts_at", _n1);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
