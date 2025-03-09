#!/bin/bash
cd ~/agent_memory/embedding_tools/storage

# ask user if they are sure
echo "are you sure you want to clear the storage?"
echo "this will remove the nexus and vector_database directories and contents"
if [ "$1" != "-y" ]; then
    read -p "are you sure? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
    exit 1
    fi
fi

echo "removing nexus and vector_database directories and contents..."
sleep 1
rm -rf nexus
rm -rf vector_database
echo "nexus and vector_database directories and contents removed."
sleep 1
echo "creating nexus and vector_database directories for next time..."
sleep 1
mkdir nexus
mkdir vector_database
echo "mt nexus and vector_database directories recreated."
echo
