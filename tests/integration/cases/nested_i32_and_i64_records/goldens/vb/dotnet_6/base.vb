Imports System.Collections.Generic
Module Check
    Dim my_data = New Object() {
        New Object() {New Dictionary(Of String, Object) From {{"value", 1}}},
        New Object() {New Dictionary(Of String, Object) From {{"value", 1099511627776}}}
    }
End Module
