#!/usr/bin/env bash
# =====================================================================
# Deploy Agent Spark to Hugging Face Spaces
# =====================================================================
# Prerequisites: a HF token from https://huggingface.co/settings/tokens
#
# Usage:
#   HF_TOKEN=hf_yourtoken bash deploy.sh
#   # or set the env var first, then: bash deploy.sh
# =====================================================================

set -euo pipefail

TOKEN="${HF_TOKEN:-}"
if [ -z "$TOKEN" ]; then
    echo "Error: HF_TOKEN not set."
    echo "  export HF_TOKEN=hf_yourtoken"
    echo "  Get a token at: https://huggingface.co/settings/tokens"
    exit 1
fi

echo "Deploying Agent Spark Playground to Hugging Face Spaces..."

# Login
python3 -c "
import os
os.environ['HF_TOKEN'] = '$TOKEN'
from huggingface_hub import HfApi, login, create_repo, upload_folder

login(token='$TOKEN', add_to_git_credential=False)
api = HfApi()

# Create or get the Space
space_id = 'agent-spark-playground'
namespace = api.whoami()['name']

print(f'Creating Space: {namespace}/{space_id}')
create_repo(
    repo_id=f'{namespace}/{space_id}',
    repo_type='space',
    private=False,
    exist_ok=True,
)

print('Uploading files...')
upload_folder(
    repo_id=f'{namespace}/{space_id}',
    folder_path='huggingface',
    repo_type='space',
    path_in_repo='.',
)

print(f'Deployed!')
print(f'https://huggingface.co/spaces/{namespace}/{space_id}')
"
