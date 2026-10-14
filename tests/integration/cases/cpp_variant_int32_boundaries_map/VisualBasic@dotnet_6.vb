Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"below", -2147483649},
        {"minimum", -2147483648},
        {"above", -2147483647},
        {"nested", New Integer() {0}}
    }
End Module
