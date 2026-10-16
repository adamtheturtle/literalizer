def main():
    var ref_data = List([
        1,
        2,
    ])
    var my_data = List([
        0,
    ])
    (void)my_data;
    my_data = ref_data.copy()
    (void)my_data;
