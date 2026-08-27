import torch
from torch import nn

X = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
Y = torch.tensor([[0.], [1.], [1.], [0.]])
Y3 = torch.tensor([0, 1, 1, 2])


def train(name, activation=nn.Tanh, classes=1, zero=False, linear=False):
    torch.manual_seed(0)
    model = (nn.Sequential(nn.Linear(2, 1)) if linear else
             nn.Sequential(nn.Linear(2, 2), activation(), nn.Linear(2, classes)))
    if zero:
        for parameter in model.parameters():
            nn.init.zeros_(parameter)
    target = Y if classes == 1 else Y3
    loss_function = nn.BCEWithLogitsLoss() if classes == 1 else nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.05)
    initial_loss = loss_function(model(X), target).item()
    print('\n' + name)
    for step in range(5000):
        optimizer.zero_grad()
        loss = loss_function(model(X), target)
        loss.backward()
        if step == 0:
            early_gradient = model[0].weight.grad.detach().clone()
        optimizer.step()
        if zero and step in [0, 1, 9, 99, 999, 4999]:
            weights = model[0].weight.detach()
            print('Step:', step + 1, 'hidden weights:', weights.tolist(),
                  'identical rows:', torch.equal(weights[0], weights[1]))
    optimizer.zero_grad()
    logits = model(X)
    final_loss = loss_function(logits, target)
    final_loss.backward()
    probabilities = (torch.sigmoid(logits) if classes == 1 else torch.softmax(logits, dim=1)).detach()
    predictions = (probabilities >= 0.5).long() if classes == 1 else probabilities.argmax(dim=1)
    correct = int((predictions == target).sum())
    print('Initial loss:', initial_loss, 'final loss:', final_loss.item())
    print('Probabilities:', probabilities.tolist())
    print('Predictions:', predictions.tolist(), 'correct:', correct, '/ 4')
    print('Early first-layer gradient:', early_gradient.tolist())
    print('Early gradient norm:', early_gradient.norm().item())
    print('Final first-layer gradient:', model[0].weight.grad.tolist())
    if classes == 3:
        print('Output weight shape:', list(model[-1].weight.shape))
        print('Probability sums:', probabilities.sum(dim=1).tolist())
        assert torch.allclose(probabilities.sum(dim=1), torch.ones(4), atol=1e-6)
    if name in ['Tanh', 'Three classes']:
        assert correct == 4
    return final_loss.item(), probabilities, correct, early_gradient


if __name__ == '__main__':
    torch.set_num_threads(1)
    train('Linear baseline', linear=True)
    for name, activation in [('Sigmoid', nn.Sigmoid), ('Tanh', nn.Tanh), ('ReLU', nn.ReLU)]:
        train(name, activation)
    train('Zero initialization', zero=True)
    train('Three classes', classes=3)
