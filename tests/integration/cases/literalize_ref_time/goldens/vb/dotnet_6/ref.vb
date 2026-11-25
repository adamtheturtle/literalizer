Imports System
Imports System.Collections.Generic
Module Check
    Dim MyTime = New TimeOnly(1, 2, 3)
    Dim my_data = New Dictionary(Of String, Object) From {
        {"x", MyTime}
    }
End Module
