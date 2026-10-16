Imports System.Collections.Generic
Module Check
    Dim ref_data = New Integer() {
        1,
        2
    }
    Dim my_data = New Integer() {
        0
    }
    (void)my_data;
    my_data = ref_data
    (void)my_data;
End Module
