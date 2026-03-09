# Headless Research Agent

## Overview

Launch a trusted headless kiro-cli instance to perform web research without requiring approval for each tool use. The subagent writes findings to a file that the parent agent can monitor and consume. Use this when you need to research topics without blocking on tool approvals.

## Parameters

- **research_query** (required): The research question or topic to investigate
- **output_file** (required): Path where the subagent should write its findings
- **model** (optional, default: "claude-sonnet-4.6"): Model to use for research (claude-opus-4.6 for complex research, claude-sonnet-4.6 for standard research)
- **timeout** (optional, default: "300"): Maximum seconds to wait for research completion

**Constraints for parameter acquisition:**
- If all required parameters are already provided, You MUST proceed to the Steps
- If any required parameters are missing, You MUST ask for them before proceeding
- When asking for parameters, You MUST request all parameters in a single prompt
- When asking for parameters, You MUST use the exact parameter names as defined

## Steps

### 1. Prepare Output Location
Ensure the output directory exists and the output file path is valid.

**Constraints:**
- You MUST create the parent directory if it doesn't exist
- You MUST use an absolute path for the output file
- You SHOULD use a `.md` extension for the output file
- You MAY create an `agentic-research/` directory in the project root for organizing research outputs

### 2. Construct Research Prompt
Build a prompt that instructs the subagent to research and write findings to the output file.

**Constraints:**
- You MUST instruct the subagent to write findings to the specified output file
- You MUST instruct the subagent to include sources/references
- You SHOULD instruct the subagent to structure findings with clear headings
- You SHOULD instruct the subagent to summarize key findings at the top
- You MAY include specific aspects to focus on based on the research query

### 3. Launch Headless Subagent
Execute kiro-cli in headless mode with trust-all enabled.

**Constraints:**
- You MUST use `--no-interactive` flag because the subagent runs without user input
- You MUST use `-a` or `--trust-all-tools` flag to avoid blocking on approvals
- You MUST use `--model` to specify the research model
- You MUST wrap the command with `timeout` to prevent runaway processes
- You SHOULD redirect stderr to capture any errors
- You MUST NOT use `&` to background the process because you need to know when it completes

**Command template:**
```bash
timeout {timeout}s kiro-cli chat --model {model} --no-interactive -a "{prompt}" 2>&1
```

### 4. Verify Output
Check that the subagent successfully wrote findings to the output file.

**Constraints:**
- You MUST check if the output file exists after the command completes
- You MUST read the output file to verify it contains research findings
- If the file is empty or missing, You MUST report the failure and include any stderr output
- You SHOULD summarize the key findings for the user
- You MAY suggest follow-up research if the findings are incomplete

## Examples

### Example 1: Git Worktrees Research
**Input:**
- research_query: "How are developers using git worktrees with Claude Code for parallel development?"
- output_file: "/Users/me/project/agentic-research/git-worktrees.md"
- model: "claude-sonnet-4.6"
- timeout: "120"

**Prompt constructed:**
```
Research the following topic and write your findings to /Users/me/project/agentic-research/git-worktrees.md

Topic: How are developers using git worktrees with Claude Code for parallel development?

Instructions:
1. Search the web for relevant information
2. Write findings to the specified file with clear headings
3. Include a summary of key findings at the top
4. Include sources/references at the bottom
5. Focus on practical workflows and real-world usage patterns
```

**Command executed:**
```bash
timeout 120s kiro-cli chat --model claude-sonnet-4.6 --no-interactive -a "Research the following topic..." 2>&1
```

### Example 2: Quick API Research
**Input:**
- research_query: "What are the rate limits for the GitHub API?"
- output_file: "/tmp/github-api-limits.md"
- model: "claude-sonnet-4.6"
- timeout: "180"

**Expected Behavior:**
Standard research using sonnet model, results written to temp file for quick consumption.

## Troubleshooting

### Subagent Times Out
If the research times out:
- Increase the timeout value for complex topics (default is 300s)
- Break complex research into smaller, focused queries
- Check if the model is responding (network issues, rate limits)

### Output File Empty or Missing
If no output is produced:
- Check stderr output for errors
- Verify the model name is valid (use `kiro-cli chat --help` to see available models)
- Ensure the output directory exists and is writable
- Try with a simpler research query to verify the workflow

### Model Not Available
If the model is not found:
- Run `kiro-cli chat --model invalid --no-interactive -a "test"` to see available models
- Use claude-sonnet-4.6 or claude-opus-4.6 (haiku and smaller models are not recommended for research)

### Research Quality Issues
If findings are incomplete or low quality:
- Use claude-opus-4.6 for complex research requiring deeper analysis
- Provide more specific research queries
- Include specific aspects to focus on in the prompt
