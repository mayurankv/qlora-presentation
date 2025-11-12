# Presentation

## Title Slide

<!-- EMPTY -->

## Introduction

Today I'm going to cover the topic of fine-tuning large language models focussing on two parameter efficient methods called LoRA and QLoRA.

LLMs have rapidly become useful in many fields, including at Lendable, due to their effectiveness in tackling a variety of problems. These involve classification, content generation, and many other capabilities straight off the shelf. These capabilities come from training regimes focussing on a wide breadth of data, however, this can mean that LLMs are not always well suited for tasks focussed on specific domains or use cases due to their generalised training regime. As a result, sometimes we may seek to adjust these models to specific roles and tasks, and this is where fine-tuning comes into play.

## Fine Tuning

> Fine-tuning an LLM is the process of adapting a pre-trained model to perform better at a specific task.

Naive fine-tuning is the relatively simple approach of taking an existing model, and continuing its training regime with the models trained weights as a starting point.
This involves updating ALL of the parameters of the model with full forwards and backpropogation passes to update the weights. This makes fine-tuning very large models extremely inefficient.
Parameter Efficient Fine-Tuning is the name given to approaches that aim to fine-tune a model by training a number of weights much smaller than the total size of the model.
Some approaches involve limiting the weights being updated or training external modules to adapt the model for a specific task, but these approaches fail to reach the naive fine-tuning baseline performnce. In addition they often introduce inference latency or reduce the models usable context window.

The diagrams shown are a simplification but appraoches which add adapter layers to the model must be run in sequence breaking the parallelism of the deep models and prompt engineering style prefix layer appraoches suffer from decreasing context windows and performance gains which are hard to map to trainable parameters.

A method of fine-tuning which doesn't suffer from these drawbacks and also attains the naive fine-tuning baseline is LoRA.

## LoRA

LoRA takes inspiration from a paper showing that over-parametrised models such as LLMs have a low intrinsic dimesnion. The approach of this paper from Microsoft hypothesises that when fine-tuning a model, the change in weights that occurs has a low intrinsic rank, hence the name Low Rank Adaptation.
This hypothesis means that you don't have to train a models weights directly, but instead a low rank representation of the CHANGES to those weights. This means you don:t have to track changes to all the weights of the model making this fine-tuning much more memory and compute efficient.
This can be represented as follows:

- For each weight matrix $\vec{h}=W\vec{x} + \vec{b}$
- We consider only the matrix multiplication component $\vec{h}=W\vec{x}$
- Rather than fine-tuning $W$ itself, we treat this as fixed $W_0$ and fine tune an additional $\Delta W$
- This $\Delta W$ is decomposed into two low rank matrices
- This leaves the new low rank matrices as trainable weights

These low rank matrices are updated through traditional gradient descent when fine-tuning the model without modifying the weights of the base model.

### LoRA: Advantages and Disadvantages

#### Advantages (LoRA)

- LoRA is a true generalisation of fine tuning in a manner which additional layers and prefix based methods aren't. Increasing the rank $r$ eventually converges to training the original model.
- It has no inference latency as we can easily calculate $W_0 + BA$ at inference time and easily change our model weights to those of a different fine-tuned model with $W_0 + B'A'$
- This decomposition also makes the weight updates more interpretable in relation to the overall model weights
- Furthermore, the paper finds that even extremely low ranks such as 1 or 2 are sufficient to attain strong fine-tuning performance for large performance gains

#### Drawbacks (LoRA)

- Reducing the dimensionality of the weight updates introduces information loss which can be comparable to overfitting
  - In practice LLMs are so over-parameterised this doesn't have a significant effect
- Determining the optimal rank hyperparameter $r$ to use can be challenging

### LoRA: Performance

Some of the results given in the paper show that GPT3 fine tuned with LoRA outperforms the other comparable methods, even improving on the baseline full fine-tuning.

Analysis within the paper suggests that this performance occurs as $\Delta W$ is able to amplify existing features in the model that are relevant to the downstream task.

## QLoRA

QLoRA stands for Quantised Low-Rank Adaptation and is an extension of LoRA which inorporates quantisation. Quantisation refers to representing a floating point number stored in a larger number of bits with fewer bits. This leads to quantisation loss but results in numbers which require less memory to operate on.
QLoRA Takes the full model and freezes the weights as in LoRA but then quantises the weights of the model to a smaller size. This can't typically be done when fine-tuning as gradients can't propogate through the quantisation operation, but since we are separately training our low rank adaptors, we can quantise these weights without issue.
Quantisation typically requires normalisation for model stability so QLoRA actually quantises not only the weights, but the normalisation scale factor - this is referred to as double quantisation.
QLoRA also benefits from storing the optimiser state (i.e. Adam parametes) in CPU freeing up GPU VRAM.

### QLoRA: Advantages and Disadvantages

#### Advantages (QLoRA)

- QLoRa enjoys most of the existing LoRA advantages
- But it also enjoys SIGNIFICANT memory savings as calculating the backpropagations results of the model on the Low Rank Adaptors is done in quantised terms
- It can achieve full baseline fine-tuning performance

#### Drawbacks (QLoRA)

- However, there are some drawbacks. The quantisation causes information loss which can impact performance.
- The restrcited representation can potentially lead to less effective models than basic LoRA due to a lower overall representability within the model
- And finally fine-tuning perforamance can be very dependent on the dataset

### QLoRA: Performance

This result from the paper shows that QLoRA is able to replicate both LoRA and full fine-tuning across a variety of models

## Discussion Points

1. LoRA low rank effectiveness - If the model is so overparameterised that even a completely rank deficient LoRA can pull out the relevant features, how is LoRA able to find that relevant feature within the myriad features of the model.
2. QLoRA quantisation degradation - Completely quantising the model to a bit would presumably result in very poor fine-tuning performance. Are there domains and tasks which are more or less sensitive to the quantisation performance loss?

## Questions

Any questions?
