Imports System.Collections.Generic
Module Check
    ' Outdented from the inner mapping too, so the root claims this.
    Dim my_data = New Dictionary(Of String, Object) From {
        {"a", New Dictionary(Of String, Object) From {{"b", New Integer() {1}}, {"c", 2}}},
        {"d", 3}
    }
End Module
