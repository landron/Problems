#!/bin/bash

set -euo pipefail
# set -x

start=$(date +%s)

go mod tidy

gofumpt -l -w -extra ./

# only tests
#   avoid
#       go: build output "Ch10_Dynamic_Programming_Fundamentals" already 
#           exists and is a directory
go build -o /dev/null ./...

go test ./...

golangci-lint run -v --timeout 600s

echo
echo "All checks passed successfully at $(date +'%H:%M:%S %d.%m')"
end=$(date +%s)
elapsed=$((end - start))
echo "Elapsed time: ${elapsed} seconds"
