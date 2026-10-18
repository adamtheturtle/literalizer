Imports System.Collections.Generic
Module Check
    Dim StringMap = New Dictionary(Of String, Object) From {
        {"k", "s"}
    }
    Dim my_data = New Object() {
        StringMap,
        New Dictionary(Of String, Object) From {{"k", 1}}
    }
End Module
