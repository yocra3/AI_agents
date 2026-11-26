# Framework principles

Design rules of the agent framework that `craftsman` keeps when it changes agents, skills,
templates, references, or their documentation; the maintaining-framework skill gives the
procedures that apply them.

1. **Behavior lives in a skill or a template.** Agents and skills never read another skill's
   private files. Material that only one skill uses, such as a template or a list of sources,
   stays in that skill; material shared by several skills or agents goes in
   `{Agents_Folder}/references/`, and a shared template in its `templates/` folder. Framework
   configuration, such as the model profiles, goes in `{Agents_Folder}/config/`. Project
   decisions, such as the toolchain or the folder layout, go in `{Agents_file}`.
2. **Each rule lives in one place.** Other files point to it instead of repeating it. When
   content moves, search for every reference to it and fix the ones left dangling.
3. **Skill or phase.** A skill holds substantial knowledge of its own, is used by several phases
   or agents, or makes sense outside an implementation plan. A procedure that only chains other
   skills inside the coordinator's flow is a phase.
4. **One source of phases.** `{Agents_Folder}/references/phases/` defines every phase and every
   delegation that is not a plan marker. Skill profiles hold conventions only, such as how code
   or tests are written. Agents do not describe phase procedures; only
   `implementation-coordinator` names markers, for its commit points, status, and stops.
5. **Common agent structure.** Every agent definition has the sections Role, Goal, Skills, its own
   sections, Boundaries, and Output, in that order. Available tools are declared only in the
   frontmatter of its source.
6. **`{Agents_file}` is brief.** The `AGENTS.md` template holds its content, the blueprint the
   values and defaults, and the project-bootstrap skill when to include each part.
7. **Documentation follows every change.** In the AI_agents repository only, each change updates
   the CHANGELOG's Unreleased section, `README.md`, and the workflow documents in `docs/` where
   they describe what changed. The detailed figure of each workflow lives in its document in
   `docs/`, and a change to a flow updates it. The figure of each workflow in `README.md` is a
   user-facing summary, which changes only when the steps that the user sees change.
8. **The CHANGELOG starts from the last release.** Every entry of the CHANGELOG's Unreleased
   section, the upgrade notes included, describes the net change from the last released version,
   never an intermediate state of the unreleased cycle. A change made and then reverted or
   renamed within the cycle appears only in its final form, or not at all. The upgrade notes say
   what an installed project must do to move from the last released version to the new one.
9. **Hyphenated names.** Agent, skill, and file names use hyphens, such as
   `implementation-coordinator`, in file names and in text. Only a generated file uses another
   form, when its environment requires it.
