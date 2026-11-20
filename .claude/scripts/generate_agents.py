# Regenerate .claude/agents/*.md from .codex/agents/*.toml.
# Usage: python3 .claude/scripts/generate_agents.py [repository-root]
import glob, os, re, sys

USAGE = "usage: python3 .claude/scripts/generate_agents.py [repository-root]"
args = sys.argv[1:]
if any(a in ("-h", "--help") for a in args):
    print(USAGE)
    sys.exit(0)
if any(a.startswith("-") for a in args) or len(args) > 1:
    sys.exit(USAGE)
root = args[0] if args else os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sources = sorted(glob.glob(os.path.join(root, ".codex", "agents", "*.toml")))
if not sources:
    sys.exit("error: no .toml agents in %s" % os.path.join(root, ".codex", "agents"))
MODELS = {"gpt-6-sol": "claude-opus-5-5", "gpt-5.6-terra": "claude-sonnet-5-5", "gpt-6-luna": "claude-haiku-5-5"}
# Per-agent Claude model overrides, keyed by hyphenated name; they take precedence over MODELS.
CLAUDE_MODELS = {"coder": "claude-sonnet-5-5", "tester": "claude-sonnet-5-5", "cleaner": "claude-sonnet-5-5"}
BASE = "Read, Grep, Glob, Skill"
TOOLS = {
    "analyst": "Write, Edit, WebSearch, WebFetch, AskUserQuestion",
    "architect": "Bash, Write, Edit, WebSearch, WebFetch, AskUserQuestion",
    "product-owner": "Write, Edit, AskUserQuestion",
    "craftsman": "Bash, Write, Edit, WebSearch, WebFetch, AskUserQuestion",
    "implementation-coordinator": "Agent(engineer, tester, coder, cleaner, reviewer, dev-ops), Bash, Edit, TodoWrite, AskUserQuestion",
    "engineer": "Bash, Write, Edit, WebFetch",
    "tester": "Bash, Write, Edit",
    "coder": "Bash, Write, Edit",
    "cleaner": "Bash, Write, Edit",
    "reviewer": "Bash",
    "dev-ops": "Bash, Write, Edit",
    "data-analyst": "Bash, Write, Edit, WebSearch, WebFetch, AskUserQuestion",
}

out_dir = os.path.join(root, ".claude", "agents")
os.makedirs(out_dir, exist_ok=True)
for path in sources:
    text = open(path).read()
    field = lambda k: re.search(r'^%s = "(.*)"$' % k, text, re.M).group(1)
    body = re.search(r'developer_instructions = """\n(.*?)"""', text, re.S).group(1)
    name = field("name").replace("_", "-")
    model = CLAUDE_MODELS.get(name) or MODELS[field("model")]
    front = [
        "---",
        "name: %s" % name,
        "description: %s" % field("description"),
        "model: %s" % model,
        "effort: %s" % field("model_reasoning_effort"),
        "tools: %s, %s" % (BASE, TOOLS[name]),
        "---",
        "",
    ]
    with open(os.path.join(out_dir, name + ".md"), "w") as fh:
        fh.write("\n".join(front) + body)
    print(name, model, field("model_reasoning_effort"))
