# CLI ownership and targeted lookup

- Binary lifecycle and embedded tools: inspect the selected CLI's `main.go` and
  `tools/tools.go`; the 0.9.0 reference index records main tool names, flag aliases
  and embedded tool names. Read the corresponding `tools/<name>.md` when present.
- OpenWhisk aliases such as `ops action`: inspect `IsWskWrapperCommand` in the
  selected CLI source (in `main.go` in the current reference). These wrappers are
  distinct from task namespaces and expose underlying wsk commands. Use matching
  wsk help for its individual options, not an invented task synopsis.
- Task commands: `docopts.md` describes accepted CLI arguments; `opsfile.yml`
  defines execution and may delegate to Bun/TypeScript or shell/Python scripts.
- Project/plugin commands: consult `OPS_ROOT_PLUGIN` and the selected project
  definitions. Scan that root independently before assuming a global command.
- Prerequisites: `prereq.go`, root and nested prerequisite definitions. CLI lookup
  can change directories into the selected task. Relative files in a task are
  therefore not necessarily resolved under the shell's original directory.

Examples of distinct ownership:

| Surface | Meaning to verify in the selected version |
| --- | --- |
| `ops -info` | Binary and active profile information |
| `ops -config` | Embedded configuration interface |
| `ops config ...` | Versioned configuration tasks |
| `ops -update` | CLI/task prerequisite update path |
| `ops update ...` | Versioned platform/update tasks |
| `ops -login` | Binary authentication flow |
| `ops ide login` | Task-driven project login |

A name in the embedded index is not an exhaustive specification of its nested
flags. Read the matching implementation/help only when needed. No automated
crawler executes commands to discover them.
