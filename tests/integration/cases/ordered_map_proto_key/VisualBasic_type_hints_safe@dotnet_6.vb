Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"__proto__", New Dictionary(Of String, Object) From {{"x", 1}}},
        {"ordinary", 2}
    }
End Module
