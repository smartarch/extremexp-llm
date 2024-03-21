# AutoML workflow with wrong implementation

We introduced a mistake into the `FailurePredictionInManufacture` workflow: In the `automl_ideko.MLTrainingAndEvaluation` subworkflow, the `ModelEvaluation` task uses `regression_evaluation.py`, but the `param metrics` contains classification metrics.

The task for the Agent is to explore the whole workflow including subworkflows and spot a mistake.

## Variants

1. Separate `xxp` files divided to packages.
2. `yaml` description files.
3. Assembled `xxp` workflows -> information from parent workflow are copied to the assembled workflow, packages are not necessary anymore.
4. Separate `xxp` files divided to packages with descriptions.
5. Assembled `xxp` workflows with descriptions.

Possible improvements:

* add list of all workflows (and subworkflows) to the system prompt.
* paste all the workflow files directly into the prompt

TODO: How can we expand the workflow? Should we just paste the subworkflow content there (and ignore that the original DSL does not allow defining new tasks inside `configure task`)?

## Results

Obtained specifications of workflows (✅ = yes, ❌ = no, ➖ = not applicable):

|Variant|FailurePredictionInManufacture|HyperparameterOptimization|TrainTestSplitValidation|MLTrainingAndEvaluation|automl.AutoML|automl.MLTrainingAndEvaluation|
|-|-|-|-|-|-|-|
|1|✅|❌|❌|✅|✅|❌|
|2|✅|✅|❌|✅|➖|➖|
|3|✅|✅|❌|✅|➖|➖|
|4|✅|❌|❌|❌|❌|❌|
|5|✅|✅|❌|✅|➖|➖|

Note that `TrainTestSplitValidation` is a subworkflow of `HyperparameterOptimization`, so to find it, subworkflows must be explored recursively.
