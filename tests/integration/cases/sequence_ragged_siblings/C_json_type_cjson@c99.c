#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateArray();
cJSON *_n1 = cJSON_CreateArray();
cJSON *_n2 = cJSON_CreateString("set_task");
cJSON_AddItemToArray(_n1, _n2);
cJSON *_n3 = cJSON_CreateString("web");
cJSON_AddItemToArray(_n1, _n3);
cJSON *_n4 = cJSON_CreateString("lint_web");
cJSON_AddItemToArray(_n1, _n4);
cJSON_AddItemToArray(_n0, _n1);
cJSON *_n5 = cJSON_CreateArray();
cJSON *_n6 = cJSON_CreateString("merge_pipelines");
cJSON_AddItemToArray(_n5, _n6);
cJSON_AddItemToArray(_n0, _n5);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
