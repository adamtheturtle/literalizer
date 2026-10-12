Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"minimum", -2147483648},
        {"neighbor", -2147483647},
        {"maximum", 2147483647},
        {"nested", New Integer() {-2147483648}}
    }
End Module
