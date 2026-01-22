import numpy as np
import pandas as pd

def train_val_test_split(X, y, train=0.7, val=0.15, test=0.15, seed=42):
    assert abs(train + val + test - 1.0) < 1e-12
    rng = np.random.default_rng(seed)
    n = X.shape[0]
    idx = rng.permutation(n)
    n_train = int(train * n)
    n_val = int(val * n)

    i_train = idx[:n_train]
    i_val   = idx[n_train:n_train + n_val]
    i_test  = idx[n_train + n_val:]

    return (X[i_train], y[i_train]), (X[i_val], y[i_val]), (X[i_test], y[i_test])

def mse(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=np.float64)
    y_pred = np.asarray(y_pred, dtype=np.float64)
    return np.mean((y_true - y_pred) ** 2)

def rmse(y_true, y_pred):
    return np.sqrt(mse(y_true, y_pred))

def r2(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=np.float64)
    y_pred = np.asarray(y_pred, dtype=np.float64)
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan

def sgd_linear_regression(
    X_train, y_train,
    X_val=None, y_val=None,
    lr=1e-4, epochs=200, batch_size=16,
    shuffle=True, seed=42,
    verbose_every=20
):
    """
    Linear regression: y_hat = X w + b
    SGD with mini-batches (batch_size can be 1 for pure SGD, or n for full-batch GD).
    Uses float64 throughout for numerical consistency.
    """
    X_train = np.asarray(X_train, dtype=np.float64)
    y_train = np.asarray(y_train, dtype=np.float64).reshape(-1)

    n, d = X_train.shape
    rng = np.random.default_rng(seed)

    # Initialize parameters
    w = rng.normal(0.0, 0.01, size=d).astype(np.float64)
    b = np.float64(0.0)

    history = {
        "epoch": [],
        "train_mse": [],
        "train_rmse": [],
        "train_r2": [],
        "val_mse": [],
        "val_rmse": [],
        "val_r2": [],
    }

    def predict(X):
        X = np.asarray(X, dtype=np.float64)
        return X @ w + b

    for epoch in range(1, epochs + 1):
        if shuffle:
            idx = rng.permutation(n)
            X_ep = X_train[idx]
            y_ep = y_train[idx]
        else:
            X_ep = X_train
            y_ep = y_train

        # iterate mini-batches
        for start in range(0, n, batch_size):
            end = min(start + batch_size, n)
            Xb = X_ep[start:end]
            yb = y_ep[start:end]

            yhat = Xb @ w + b
            err = yhat - yb
            m = Xb.shape[0]

            # Gradients of MSE: (1/m) * sum (yhat - y)^2
            # d/dw = (2/m) * X^T (yhat - y)
            # d/db = (2/m) * sum (yhat - y)
            grad_w = (2.0 / m) * (Xb.T @ err)
            grad_b = (2.0 / m) * np.sum(err)

            w -= lr * grad_w
            b -= lr * grad_b

        # record metrics per epoch
        yhat_train = predict(X_train)
        tr_mse = mse(y_train, yhat_train)
        tr_rmse = np.sqrt(tr_mse)
        tr_r2 = r2(y_train, yhat_train)

        if X_val is not None and y_val is not None:
            y_val = np.asarray(y_val, dtype=np.float64).reshape(-1)
            yhat_val = predict(X_val)
            va_mse = mse(y_val, yhat_val)
            va_rmse = np.sqrt(va_mse)
            va_r2 = r2(y_val, yhat_val)
        else:
            va_mse = va_rmse = va_r2 = np.nan

        history["epoch"].append(epoch)
        history["train_mse"].append(tr_mse)
        history["train_rmse"].append(tr_rmse)
        history["train_r2"].append(tr_r2)
        history["val_mse"].append(va_mse)
        history["val_rmse"].append(va_rmse)
        history["val_r2"].append(va_r2)

        if verbose_every and (epoch % verbose_every == 0 or epoch == 1 or epoch == epochs):
            if np.isfinite(va_mse):
                print(f"Epoch {epoch:4d} | train RMSE={tr_rmse:8.2f}, R2={tr_r2:6.3f} | val RMSE={va_rmse:8.2f}, R2={va_r2:6.3f}")
            else:
                print(f"Epoch {epoch:4d} | train RMSE={tr_rmse:8.2f}, R2={tr_r2:6.3f}")

    return w, b, pd.DataFrame(history)

def evaluate_linear_model(X, y, w, b):
    X = np.asarray(X, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64).reshape(-1)
    yhat = X @ w + b
    return {
        "MSE": mse(y, yhat),
        "RMSE": rmse(y, yhat),
        "R2": r2(y, yhat),
    }

def make_synthetic_linear(n=1000, d=5, noise_sd=0.5, seed=42):
    """
    make_synthetic_linear generates a synthetic linear regression dataset with known true parameters, so you can test whether an optimization algorithm (like SGD) can recover them.
    
    n — number of observations
    d — number of features (dimensions)
    noise_sd — standard deviation of observational noise
    seed — random number generator seed
    """
    rng = np.random.default_rng(seed)
    X = rng.normal(0, 1, size=(n, d)).astype(np.float64)
    w_true = rng.normal(0, 2, size=d).astype(np.float64)
    b_true = np.float64(rng.normal(0, 1))
    y = (X @ w_true + b_true + rng.normal(0, noise_sd, size=n)).astype(np.float64)
    return X, y, w_true, b_true

