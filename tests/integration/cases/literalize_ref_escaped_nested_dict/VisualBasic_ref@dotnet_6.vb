Imports System.Collections.Generic
Module Check
    Dim Existing = 1
    Dim my_data = New Dictionary(Of String, Object) From {
        {"nested", New Integer() {0, Existing}}
    }
End Module
