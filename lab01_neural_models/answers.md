# Neural models lab

Task 1

The input space is {0,1}² and the output is either 0 or 1. The four examples are (0,0) -> 0, (0,1) -> 1, (1,0) -> 1 and (1,1) -> 0. So the warning is on exactly when the sensors disagree.

The class-1 points are at opposite corners of the square, and the class-0 points occupy the other two corners. A single straight line cannot put both class-1 points on one side and both class-0 points on the other. A single affine layer followed by sigmoid therefore cannot correctly classify all four points. On balanced XOR its best BCE is about log(2), with probabilities near 0.5.

Adding more affine layers does not fix this because their composition is still affine. XOR tests whether the model has a suitable nonlinear representation, rather than just whether it has many parameters.

Tasks 2 and 3

The model has 2 inputs, 2 tanh hidden units and 1 output logit. Sigmoid converts the logit to a binary probability. BCEWithLogitsLoss is used for training, so sigmoid is not applied separately before the loss. Adam uses learning rate 0.05, seed 0 and 5000 full-batch CPU steps.

The hidden activation is needed to make a nonlinear decision boundary possible. Sigmoid and binary cross-entropy fit the yes/no target because the output represents the probability of class 1. The hidden units do not have their own target labels. Backpropagation adjusts their weights according to how their outputs affect the final error.

The learning checks are a final loss below 0.02, all four labels correct at threshold 0.5, and a nonzero early gradient followed by a substantial decrease in loss. A nonzero gradient by itself would not show that the network has learned XOR.

In the code, `model(X)` is the forward pass and `loss_function(...)` produces the scalar loss. `loss.backward()` calculates gradients, `optimizer.step()` changes the weights and `zero_grad()` clears the previous gradients. The architecture, labels and loss choice can be checked by reading the code. Whether training converges and what gradients it produces require actually running it.

Task 4

For tanh, the initial loss was 0.715159 and the final loss was 0.00002378. Final probabilities and predictions were:

- (0,0): probability 0.00001674, prediction 0.
- (0,1): probability 0.99997115, prediction 1.
- (1,0): probability 0.99996519, prediction 1.
- (1,1): probability 0.00001448, prediction 0.

All four labels were correct. The early first-layer gradient was approximately [[0.000505, 0.000607], [-0.042569, -0.044773]]. `parameter.grad` stores the derivative of loss with respect to that parameter. It shows how a small parameter change affects loss, rather than being the optimizer's update itself. Since the loss is the mean over four inputs, its gradient is the mean of the four input-wise gradients.

With all weights and biases initialized to zero, both hidden weight rows stayed [0,0] at steps 1, 2, 10, 100, 1000 and 5000. All output probabilities stayed at 0.5 and the loss stayed at about 0.693147. Identical units get identical updates, so they cannot start learning different features. Here zero output weights block the gradient to the hidden layer, and the balanced XOR labels also give zero average output-bias gradient. Random initialization breaks the symmetry.

Changing only the hidden activation, with the same seed and training settings, gave:

- Sigmoid: final loss 0.477397, 3 of 4 correct, early first-layer gradient norm 0.000891.
- Tanh: final loss 0.00002378, 4 of 4 correct, early gradient norm 0.061785.
- ReLU: final loss 0.693147, 2 of 4 correct, early gradient norm 0.001699.

Tanh learned the task in this run; the other two did not learn all four labels. This does not prove tanh is always the best activation. Saturated sigmoid units have outputs close to 0 or 1 and small derivatives. Inactive ReLU units have negative pre-activations and zero outputs. Inspecting both pre-activations and outputs distinguishes these causes of small gradients.

Task 5

For three classes, labels become [0,1,1,2]: neither sensor active, sensors disagree, both active. The hidden layer still has two tanh units. The output now has three logits and a 3 by 2 weight matrix. CrossEntropyLoss takes these logits directly, while softmax is used to display probabilities.

The probabilities below are in class order [0,1,2]:

- (0,0): [0.99998605, 0.00001391, approximately 0], predicted class 0.
- (0,1): [0.00000663, 0.99999142, 0.00000194], predicted class 1.
- (1,0): [0.00000656, 0.99999166, 0.00000183], predicted class 1.
- (1,1): [0.00000007, 0.00001262, 0.99998724], predicted class 2.

Loss fell from 1.059108 to 0.00001091 and all four predictions were correct. The unrounded probability row sums were about [0.99999994, 1.0, 1.0, 0.99999994]. Softmax sums to one because each exponential is divided by the sum of all exponentials.

For one input, cross-entropy is -log of the target-class probability. Differentiating it through softmax gives p - y for each logit, where y is the one-hot target. With mean batch loss, this is also divided by the batch size. The target-class logit gets a negative gradient when its probability is below 1, pushing it upwards during gradient descent; other logits get positive gradients.

Adding a common constant to all logits cancels between the softmax numerator and denominator. Stable implementations use this property to subtract the maximum logit before exponentiating, avoiding overflow.

For next-token prediction, logits, softmax, cross-entropy and the p - y gradient remain the same ideas. The output has one class per vocabulary token, and a much larger model must represent the preceding context.

Reflection

1. Depth without nonlinearity still gives an affine model. XOR needs nonlinear hidden features, so extra linear layers alone cannot solve it.

2. The successful tanh run had both a large loss reduction and four correct predictions. That shows useful learning, whereas a nonzero gradient alone would only show that some parameters can change the loss.

3. Identical hidden units calculate the same outputs and receive the same updates. Random initialization lets them develop different features instead of staying copies of each other.

4. The measured gradient norms changed with activation, with tanh giving the largest early norm here. The chain rule explains how activation derivatives affect gradients, but the actual norms also depend on the weights and inputs. This one run cannot establish a universal ranking.

5. The output and loss must agree with the target. Binary classification uses one sigmoid probability with BCE, whereas mutually exclusive multiclass classification uses several logits with softmax cross-entropy.

6. The LLM helped produce the training loop and gradient-printing code. Execution was essential because a correctly shaped network can still fail to learn, as the sigmoid and ReLU runs show.

7. For a larger model, keep loss trends, prediction checks, shape checks, finite-gradient checks and probability sums. Exhaustively checking every parameter with finite differences would become too expensive because it needs many extra forward passes.
