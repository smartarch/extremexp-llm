# LLM Evaluation

This folder contains sample test instances for evaluating a LLM-based Agent. The instances are manually created based on the [*test instance patterns*](/patterns.md).

The evaluation can be run via the [`main.py`](main.py) file (assuming the necessary dependencies were installed as instructed in [installation](/README.md#Installation)).

The test instances depend on the architecture specifications defined in the [`examples`](/examples/) folder. There are currently three variants of the architecture specification DSL to test. The desired variant is set by the `variant` variable in the [`main.py`](main.py) file.

## DSL Variants

### Variant 1: separate files

The first variant is the DSL developed for the XXP project. In this variant, there can be workflows derived from other workflows. In the derived workflow (called *assembled* in the project), the configuration of the tasks can be updated, but no new control flow or data flow can be added. To fully understand the derived workflow (especially to be able to reason about the control and data flow), it is necessary to obtain the specification of the base workflow (which is referenced from the derived workflow).

The tasks can either be *primitive* (an implementation file is specified) or *composite* (composed of other tasks). For the composite tasks, a reference to a sub-workflow is specified where the sub-tasks are defined.

An example workflow specification can be found in the [`/examples/artificial_workflow/1_separate_files`](/examples/artificial_workflow/1_separate_files/) folder.

### Variant 2: assembled

The second variant is a simplified version of the first variant, where only *assembled* workflows exist. Instead of referencing the base workflow, all the information are copied into the specification of the derived workflow (and slightly syntactically simplified).

An example workflow specification can be found in the [`/examples/artificial_workflow/2_assembled`](/examples/artificial_workflow/2_assembled/) folder.

### Variant 3: expanded

The third variant is created from the second variant by inlining all the sub-workflows. Instead of a reference to a sub-workflow, the whole specification is copied inside the composite task. This can lead to a high level of nesting of tasks.

An example workflow specification can be found in the [`/examples/artificial_workflow/3_expanded`](/examples/artificial_workflow/3_expanded/) folder.
