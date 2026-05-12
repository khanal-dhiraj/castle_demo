FROM node:22-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y \
  git \
  curl \
  jq \
  python3 \
  python3-pip \
  python3-venv \
  && rm -rf /var/lib/apt/lists/*

# Install GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
  | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
  && apt-get update && apt-get install -y gh \
  && rm -rf /var/lib/apt/lists/*

# Build-args for UID/GID alignment: sandcastle docker build-image
# defaults these to the host user's UID/GID so image-built files
# and bind-mounted files share an owner without runtime chown.
ARG AGENT_UID=1000
ARG AGENT_GID=1000

# Rename the base image's "node" user to "agent" and align UID/GID.
# On macOS hosts, the default GID is 20 which collides with Debian's "dialout"
# group — drop any pre-existing group sitting on the target GID first.
RUN existing=$(getent group $AGENT_GID | cut -d: -f1) \
  && if [ -n "$existing" ] && [ "$existing" != "node" ]; then groupdel "$existing"; fi \
  && groupmod -g $AGENT_GID node \
  && usermod -u $AGENT_UID -g $AGENT_GID -d /home/agent -m -l agent node
USER ${AGENT_UID}:${AGENT_GID}

# Install Claude Code CLI
RUN curl -fsSL https://claude.ai/install.sh | bash

# Pre-create a Python venv with the SSG's runtime + test dependencies. Pre-installing
# means the bind-mounted workspace doesn't need a fresh `pip install` on every run,
# and putting the venv first on PATH makes `pip`/`pytest` use it implicitly.
RUN python3 -m venv /home/agent/.venv \
  && /home/agent/.venv/bin/pip install --no-cache-dir \
    'markdown-it-py>=3.0' \
    'python-frontmatter>=1.1' \
    'jinja2>=3.1' \
    'pygments>=2.17' \
    'pytest>=8.0'

# Venv first so `pip`/`pytest` resolve there; Claude Code CLI second.
ENV PATH="/home/agent/.venv/bin:/home/agent/.local/bin:$PATH"

WORKDIR /home/agent

# In worktree sandbox mode, Sandcastle bind-mounts the git worktree at /home/agent/workspace
# and overrides the working directory to /home/agent/workspace at container start.
# Structure your Dockerfile so that /home/agent/workspace can serve as the project root.
ENTRYPOINT ["sleep", "infinity"]
