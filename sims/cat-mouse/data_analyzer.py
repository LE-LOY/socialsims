import gc
import time
from sklearn import linear_model

def analyze(trials=100, steps=10, runs=10):
    start = time.time()

    layers = int(trials / steps)
    X = []
    Y = []

    for depth in range(1, 5):
        for run in range(1, 1 + 1):
            with open("data/" + str(depth) + "/data" + str(run) + ".txt") as f:
                for line in f.readlines():
                    line = list(map(int, line.split()))
                    for i in range(2, 12):
                        X.append([(i - 1) * steps, depth, line[0]/10, line[1]/10])
                        Y.append(line[i])

    '''lin_reg = linear_model.LinearRegression(n_jobs=-1)
    lin_reg.fit(X, Y)

    print(str(round(lin_reg.intercept_, 2)) + " + " + \
          str(round(lin_reg.coef_[0], 2)) + "*step + " + \
          str(round(lin_reg.coef_[1], 2)) + "*depth + " + \
          str(round(lin_reg.coef_[2], 2)) + "*alpha + " + \
          str(round(lin_reg.coef_[3], 2)) + "*gamma")

    print("R-squared:", str(round(lin_reg.score(X, Y), 4)))
    print()'''

    print(len(X))
    log_reg = linear_model.LogisticRegression(verbose=10, C=1e10, tol=1e-7, max_iter=1000)
    log_reg.fit(X, Y)
    print()

    # print(log_reg.coef_)
    # print(log_reg.intercept_)

    with open('data/coef.txt', 'w') as f:
        f.write('\n'.join(' '.join(map(str, line)) for line in log_reg.coef_))
    with open('data/intercept.txt', 'w') as f:
        f.write(' '.join(map(str, log_reg.intercept_)))
    with open('data/r-squared.txt', 'w') as f:
        f.write(str(log_reg.score(X, Y)))

    print("R-squared:", round(log_reg.score(X, Y), 4))
    X_test = [[0, 1, 0.5, 0.5], [50, 1, 0.5, 0.5], [100, 1, 0.5, 0.5]]
    print(log_reg.predict(X_test))

    print("time taken:", time.time() - start)

if __name__ == '__main__':
    analyze()
