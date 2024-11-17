#!/bin/bash

# Check if workflow name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <workflow-name>"
    echo "Example: $0 ci.yml"
    exit 1
fi

WORKFLOW_NAME=$1

# Get the latest run of the specified workflow
echo "Checking status of workflow: $WORKFLOW_NAME"
gh run list --workflow=$WORKFLOW_NAME --limit=1 --json status,conclusion,createdAt,updatedAt,headBranch,displayTitle \
    | jq -r '.[] | "Status: \(.status)\nConclusion: \(.conclusion)\nBranch: \(.headBranch)\nTitle: \(.displayTitle)\nCreated: \(.createdAt)\nLast Update: \(.updatedAt)"'

# If you want to watch the workflow progress
if [ "$2" = "--watch" ]; then
    echo -e "\nWatching workflow progress (Ctrl+C to stop)..."
    while true; do
        clear
        gh run list --workflow=$WORKFLOW_NAME --limit=1 --json status,conclusion,createdAt,updatedAt,headBranch,displayTitle \
            | jq -r '.[] | "Status: \(.status)\nConclusion: \(.conclusion)\nBranch: \(.headBranch)\nTitle: \(.displayTitle)\nCreated: \(.createdAt)\nLast Update: \(.updatedAt)"'
        
        # Check if workflow is completed
        STATUS=$(gh run list --workflow=$WORKFLOW_NAME --limit=1 --json status | jq -r '.[].status')
        if [ "$STATUS" = "completed" ]; then
            CONCLUSION=$(gh run list --workflow=$WORKFLOW_NAME --limit=1 --json conclusion | jq -r '.[].conclusion')
            echo -e "\nWorkflow completed with conclusion: $CONCLUSION"
            break
        fi
        
        # Show countdown with dots
        for i in {5..1}; do
            echo -ne "\r$(yes . | head -n $i | tr -d '\n')"
            sleep 1
        done
        echo -ne "\r     \r"
    done
fi
