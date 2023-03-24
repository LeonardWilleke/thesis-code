#!/bin/bash
cd "${0%/*}" || exit
set -e
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

#------------------------------------------------------------------------------

(
    runApplication setExprBoundaryFields
    runApplication $(getApplication)
)