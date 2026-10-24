Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"test", New Object() {5, New String() {"compile", "test"}}},
        {"package", New Object() {7, New String() {"link", "test"}}}
    }
End Module
