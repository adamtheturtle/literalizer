Imports System.Collections.Generic
Module Check
    Dim item = New Integer() {
        1,
        2
    }
    Dim my_data = New Integer() {
        1,
        2
    }
    (void)my_data;
    my_data = item
    (void)my_data;
End Module
