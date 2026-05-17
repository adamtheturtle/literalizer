Imports System
Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"exact_millisecond", New TimeOnly(9, 30, 15, 123)},
        {"sub_millisecond", New TimeOnly(9, 30, 15, 123, 456)}
    }
End Module
