Before writing or changing one of the project's own nf-core-style modules or subworkflows, never an
imported one, load the specifications relevant to its type and the aspects being changed. For a
module, start with General, Naming conventions, and Input/output options; also load Documentation,
Module parameters, Resource requirements, Software requirements, and Formatting when the change
affects those concerns. For a subworkflow, start with General, Naming conventions, and Input/output
options; also load Subworkflow parameters, Documentation, and Formatting when applicable. nf-test
requirements for modules and subworkflows belong to the testing-unit skill.

## Module specifications

The following specifications define standards for developing nf-core modules:

- **[General](../nextflow-guidelines/modules/general.md):** Foundation for module development including input/output handling, `ext.args`, multi-tool piping, compression, version emission, and script templating.
- **[Naming conventions](../nextflow-guidelines/modules/naming-conventions.md):** Standards for naming module files, processes, parameters, functions, channels, and outputs.
- **[Input/output options](../nextflow-guidelines/modules/input-output-options.md):** Guidelines for defining input channels, output emissions, and handling optional inputs and outputs.
- **[Documentation](../nextflow-guidelines/modules/documentation.md):** Requirements for `meta.yml` files including tool descriptions, keywords, and ontology integration.
- **[Module parameters](../nextflow-guidelines/modules/module-parameters.md):** Guidelines for parameter usage ensuring modules remain flexible and reusable across different pipeline contexts.
- **[Resource requirements](../nextflow-guidelines/modules/resource-requirements.md):** Standards for specifying computational resources through process labels and the `task` directive.
- **[Software requirements](../nextflow-guidelines/modules/software-requirements.md):** Guidelines for declaring software dependencies using Conda, Docker, and Singularity through BioContainers.
- **[Formatting](../nextflow-guidelines/modules/formatting.md):** Requirements for Nextflow syntax formatting, lint-clean code, and general code layout.

## Subworkflow specifications

The following specifications define standards for developing nf-core subworkflows:

- **[General](../nextflow-guidelines/subworkflows/general.md):** Foundation for subworkflow development including minimum subworkflow size and version reporting through topics.
- **[Naming conventions](../nextflow-guidelines/subworkflows/naming-conventions.md):** Standards for naming subworkflow files, parameters, functions, channels, and input/output structures.
- **[Input/output options](../nextflow-guidelines/subworkflows/input-output-options.md):** Guidelines for defining required input and output channels, and handling optional inputs.
- **[Subworkflow parameters](../nextflow-guidelines/subworkflows/subworkflow-parameters.md):** Guidelines for parameter usage ensuring subworkflows remain flexible and reusable across different pipeline contexts.
- **[Documentation](../nextflow-guidelines/subworkflows/documentation.md):** Requirements for documenting channel structures in code comments and `meta.yml` files.
- **[Formatting](../nextflow-guidelines/subworkflows/formatting.md):** Requirements for Nextflow syntax formatting, lint-clean code, and general code layout.
