import numpy as np
import sys, time

class svm:

    def __init__(self, x, y, epochs=200, learning_rate=0.01):
        self.x = np.c_[np.ones((x.shape[0])), x]
        self.y = y
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.w = np.random.uniform(size=np.shape(self.x)[1], )

    def get_loss(self, x, y):
        loss = max(0, 1 - y * np.dot(x, self.w))
        return loss

    def cal_sgd(self, x, y, w):
        if y * np.dot(x, w) < 1:
            w = w - self.learning_rate * (-y * x)
        else:
            w = w
        return w

    def train(self):
        for epoch in range(self.epochs):
            randomize = np.arange(len(self.x))
            np.random.shuffle(randomize)
            x = self.x[randomize]
            y = self.y[randomize]
            loss = 0
            for xi, yi in zip(x, y):
                loss += self.get_loss(xi, yi)
                self.w = self.cal_sgd(xi, yi, self.w)
            # print('epoch: {0} loss: {1}'.format(epoch, loss))

    def predict(self, x):
        x_test = np.c_[np.ones((x.shape[0])), x]
        return np.sign(np.dot(x_test, self.w))


if __name__ == '__main__':
    train_data_path = sys.argv[1]
    test_data_path = sys.argv[2]
    time = sys.argv[4]

    train_data = np.loadtxt(train_data_path)
    x = train_data[:, :-1]
    y = train_data[:, -1]

    test_x = np.loadtxt(test_data_path)

    # correct_y = y

    svm_ins = svm(x, y, 400)
    svm_ins.train()
    result_y = svm_ins.predict(test_x)
    # count = 0
    for i in range(result_y.size):
        print(int(result_y[i]))
        # if result_y[i] == correct_y[i]:
        #     count += 1

    # print(count / result_y.size)
