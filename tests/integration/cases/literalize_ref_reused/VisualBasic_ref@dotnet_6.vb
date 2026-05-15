Imports System.Collections.Generic
Module Check
    Dim SharedVar = New Dictionary(Of String, Object) From {
        {"_", "_"}
    }
    Dim my_data = New Object() {
        SharedVar,
        SharedVar
    }
End Module
