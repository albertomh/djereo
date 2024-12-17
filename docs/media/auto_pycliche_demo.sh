#!/bin/bash

# Types out a 'copier copy' command using the pycliche template and runs it.

target_dir="my_project"

if [ -d "$target_dir" ]; then
  rm -rf "$target_dir"
fi

sleep 3

command="uvx copier copy --trust gh:albertomh/pycliche my_project"

printf "\n"
printf "❯ %s" "$current_prompt"

for ((i=0; i<${#command}; i++)); do
  printf "%s" "${command:$i:1}"
  sleep 0.025
done

eval "$command"
