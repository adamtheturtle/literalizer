Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"single_map", New Object() {
            New Dictionary(Of String, Object) From {}
        }},
        {"single_list", New Object() {
            New Integer() {
                1
            }
        }},
        {"single_deep", New Object() {
            New Integer()() {
                New Integer() {
                    2
                }
            }
        }}
    }
End Module
