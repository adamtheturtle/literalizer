Imports System.Collections.Generic
Module Check
    ' This comment describes the last pair.
    Dim my_data = New Object() {
        New Object() {New Dictionary(Of String, Object) From {{"item", "existing"}}, "kept"},
        New Object() {New Dictionary(Of String, Object) From {{"item", "next"}}, "also kept"},
        New Object() {New Dictionary(Of String, Object) From {{"item", "last"}}, "kept too"}
    }
End Module
