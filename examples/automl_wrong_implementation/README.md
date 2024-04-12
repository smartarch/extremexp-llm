# AutoML workflow with wrong implementation

The workflows in this folder intentionally contain mistakes. The LLM is asked to find them.

The mistakes are:

* In the description of main workflow (`FailurePredictionInManufacture`), the ML goal is "binary classification", but the descriptions (and implementation) in `MLTrainingAndEvaluation` claim it is "regression".
* The description of `DataRetrieval` task in `FailurePredictionInManufacture` is wrong (does not correspond to the name of the task).
* The `ModelEvaluation` task in `MLTrainingAndEvaluation` uses `regression_evaluation.py`, but the `param metrics` contains classification metrics.

---

**Note that the rest of this document contains old results.**

---

## Variants

1. Separate `xxp` files divided to packages (`examples/automl_wrong_implementation/1_config.yaml`).
2. Assembled `xxp` workflows -> information from parent workflow are copied to the assembled workflow, nested specification is separated to the subworkflow files, packages are not necessary anymore (`examples/automl_wrong_implementation/2_config.yaml`).
3. Expanded workflow: one `xxp` file with nested subworkflows (`examples/automl_wrong_implementation/3_config.yaml`).
4. 1\. with descriptions (`examples/automl_wrong_implementation/4_config.yaml`).
5. 2\. with descriptions (`examples/automl_wrong_implementation/5_config.yaml`).
6. 3\. with descriptions (`examples/automl_wrong_implementation/6_config.yaml`).

## Goal: identify errors

We introduced a mistake into the `FailurePredictionInManufacture` workflow: In the `automl_ideko.MLTrainingAndEvaluation` subworkflow, the `ModelEvaluation` task uses `regression_evaluation.py`, but the `param metrics` contains classification metrics.

The task for the Agent is to explore the whole workflow including subworkflows and spot a mistake.

### Prompt

Read through the specification of the experiment workflow including all its subworkflows (recursively) and parent workflows.
Identify potential errors in the workflow specification and present a list of them. For each error, report to which task it is related.

Make sure that you read and analyze all the specification files before presenting the list of errors. Only present errors which come from the specifications of the workflows.

#### Follow up

##### Separate files

You did not explore the subworkflows of `AutoML`. You need to explore all the subworkflows recursively.

##### Assembled

You did not explore all the subworkflows of `FailurePredictionInManufacture`. You need to explore all the subworkflows recursively.

### Expected result

Report the error of using classification metrics with `regression_evaluation.py` inside `MLTrainingAndEvaluation`.

For the variants with descriptions, it could also be spotted that the main workflow claims the goal should be "prediction of machine failures (binary classification)", while the implementation is `regression_training.py` and `regression_evaluation.py`.

### Results (`gpt-4-0125-preview`)

#### Errors found

✅ = during first prompt, ☑️ = during follow up, ❌ = no, ➖ = not applicable

| Variant | Wrong metrics | Description mismatch | Reasonable errors / Reported errors |
|---------|----|---|---|
| 1       | ❌ | ➖ | 1/5 + 0/6 |
| 2       | ✅[^1] | ➖ | 4/6 + 7/7 |
| 3       | ✅[^1] | ➖ | 6/6 |
| 4       | ✅ | ✅ | 2/3 + 4/5 |
| 5       | ✅ | ✅ | 5/5 + 4/4 |
| 6       | ✅ | ✅ | 6/6[^2] |

The errors reported after the follow-up prompt often repeat the errors already shown after the first prompt.

[^1]: Suggests checking if metrics are appropriate for the problem at hand but does not point out the mismatch between the classification metrics and regression implementation.

[^2]: One of the recommendation is to modularize the workflow to avoid repetition... that is done in Variant 5.

#### Obtained specifications of workflows

✅ = during first prompt, ☑️ = during follow up, ❌ = no, ➖ = not applicable

|Variant|`FPIM`|`ai.MLTAE`|`AML`|`HO`|`TTSV`|`a.MLTAE`|
|-|-|-|-|-|-|-|
|1|✅|✅|✅|☑️|❌|☑️|
|2|✅|✅|➖|✅|☑️|➖|
|3|✅|➖|➖|➖|➖|➖|
|4|✅|✅|✅|☑️|☑️|☑️|
|5|✅|✅|➖|✅|❌|➖|
|6|✅|➖|➖|➖|➖|➖|

The header of the table are shortened names of workflows (`ai.MLTAE` -> `automl_ideko.MLTrainingAndEvaluation`).

## Old Results

Results for older version of the prompt, `gpt-3.5-turbo` and also `YAML` descriptions are [here](https://github.com/smartarch/extremexp-llm/blob/aba0fa76b74df79e81030d5cdd1b56eaab514252/examples/automl_wrong_implementation/README.md).
