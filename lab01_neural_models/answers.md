# Neural models

## Tasks 1–3: XOR and the model

XOR outputs 1 when the two inputs differ: (0,0): 0, (0,1): 1, (1,0): 1, (1,1): 0.

The two classes are at opposite corners of a square. One straight line cannot separate them. Adding only linear layers still gives a linear model, so a nonlinear hidden layer is needed.

The network has 2 inputs, 2 hidden units and 1 output. The hidden activation is tanh. Sigmoid turns the output into a probability. BCEWithLogitsLoss takes the raw output and applies the sigmoid internally.

Training uses Adam, learning rate 0.05, seed 0 and 5000 steps. The four inputs are trained together. Hidden units have no separate targets; backpropagation updates them using the output loss.

In the code, `model(X)` is the forward pass, `loss.backward()` computes gradients and `optimizer.step()` updates weights. `zero_grad()` clears old gradients.

## Task 4: Results

Tanh loss fell from 0.715159 to 0.00002378. All four predictions were correct. The probabilities for (0,0), (0,1), (1,0), (1,1) were about 0.000017, 0.999971, 0.999965 and 0.000014.

The early first-layer gradient was approximately [[0.000505, 0.000607], [-0.042569, -0.044773]]. A gradient tells us how loss changes with a weight. It is not the weight update itself. With mean loss, it is averaged over the four examples.

With all weights and biases set to zero, the hidden units stayed identical. The outputs remained 0.5 and loss stayed about 0.693147. Zero output weights block the hidden gradients, and balanced targets give zero output-bias gradient. Random initialization breaks this symmetry.

Keeping the same seed and training settings:

- Sigmoid: loss 0.477397, 3/4 correct, early gradient norm 0.000891.
- Tanh: loss 0.00002378, 4/4 correct, early gradient norm 0.061785.
- ReLU: loss 0.693147, 2/4 correct, early gradient norm 0.001699.

Tanh worked best in this run. Sigmoid saturation and inactive ReLU units can reduce gradients. A nonzero gradient alone does not guarantee successful training.

## Task 5: Three classes

The labels are now [0,1,1,2]: both inactive, different inputs, both active. The output layer has 3 logits and its weight matrix is 3 by 2. CrossEntropyLoss takes the logits directly; softmax is used to show probabilities.

Loss fell from 1.059108 to 0.00001091. Predictions were [0,1,1,2], so all four were correct. Each probability row summed to approximately 1.

Softmax divides each exponential by their total. Adding the same constant to all logits does not change it. Subtracting the largest logit avoids overflow. The cross-entropy gradient with respect to logits is p minus the one-hot target, divided by batch size for mean loss.

Next-token prediction uses the same logits, softmax and cross-entropy idea, but with a larger vocabulary and a representation of the previous tokens.

## Reflection

1. Nonlinearity makes XOR possible; extra linear layers alone do not.
2. Falling loss and correct predictions show useful learning, rather than just nonzero gradients.
3. Identical hidden units receive identical updates and cannot learn different features.
4. Activation derivatives affect gradients, along with weights and inputs.
5. Binary and multiclass tasks need matching output layers and losses.
6. The LLM helped with the training loop. Running it was needed to check the predictions.
7. For a larger model, check loss, predictions, shapes, finite gradients and probability sums.
