Imports System.Collections.Generic
Module Check
    Dim x As Object = New Object() {
        New Dictionary(Of String, Object) From {{"key", "hello   world"}, {"value", 1}}
    }
End Module
