Imports System.Collections.Generic
Module Check
    Dim my_data = New Object() {
        New Dictionary(Of String, Object) From {
            {"item", "existing"}
            ' This comment describes the next item.
        },
        New Dictionary(Of String, Object) From {{"item", "next"}}
    }
End Module
