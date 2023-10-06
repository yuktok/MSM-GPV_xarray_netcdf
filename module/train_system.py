from collections import defaultdict
from torch.optim.optimizer import Optimizer
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error

import torch
import torch.nn as nn
import torch.nn.functional as F
import pandas as pd
import numpy as np
DEVICE = torch.device("cuda")

from time import time
## train
def train(
    model: nn.Module,
    optimizer: Optimizer,
    train_loader: torch.utils.data.DataLoader
) -> pd.Series:
    
    # train にすることで model 内の学習時にのみ有効な機構が有効になります (Dropouts Layers、BatchNorm Layers...)
    model.train()

    criterion = nn.MSELoss()

    # ロスの値を保存する用に dict を用意
    metrics = defaultdict(float)
    n_iters = len(train_loader)

    for i, (x_i, y_i) in enumerate(train_loader):        
        x_i = x_i.to(DEVICE)
        y_i = y_i.to(DEVICE).reshape(-1, 1).float()
        
        output = model(x_i)
        loss = criterion(output, y_i)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        metric_i = {
            # loss は tensor object なので item をつかって python object に戻す
            "loss": loss.item()
        }


        for k, v in metric_i.items():
            metrics[k] += v
        
        time_sta = time()

        
    for k, v in metrics.items():
        metrics[k] /= n_iters
    

    return pd.Series(metrics).add_prefix("train_")


class Timer:
    def __init__(self, logger=None, format_str='{:.3f}[s]', prefix=None, suffix=None, sep=' '):

        if prefix: format_str = str(prefix) + sep + format_str
        if suffix: format_str = format_str + sep + str(suffix)
        self.format_str = format_str
        self.logger = logger
        self.start = None
        self.end = None

    @property
    def duration(self):
        if self.end is None:
            return 0
        return self.end - self.start

    def __enter__(self):
        self.start = time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time()
        out_str = self.format_str.format(self.duration)
        if self.logger:
            self.logger.info(out_str)
        else:
            print(out_str)


def timer(logger=None, format_str='{:.3f}[s]', prefix=None, suffix=None, sep=' '):
    return Timer(logger=logger, format_str=format_str, prefix=prefix, suffix=suffix, sep=sep)

def predict(model: nn.Module, loader:  torch.utils.data.DataLoader) -> np.ndarray:
    # train とは逆で model 内の学習時にのみ有効な機構がオフになります (Dropouts Layers、BatchNorm Layers...)
    model.eval()

    predicts = []

    for x_i, y_i in loader:

        # 明示的に勾配を計算しないように指定することができます. 
        # この関数ではモデルの更新はせずに単に出力だけを使いますので勾配は不要です.

        with torch.no_grad():
            output = model(x_i.to(DEVICE))
        predicts.extend(output.data.cpu().numpy())



    pred = np.array(predicts).reshape(-1)
    return pred


def calculate_metrics(y_true, y_pred) -> dict:
    """正解ラベルと予測ラベルから指標を計算する"""
    # return regression_metrics(y_true, y_pred)

    return {
        'rmse': mean_squared_error(y_true, y_pred) ** .5
    }


def valid(
    model: nn.Module, 
    y_valid: np.ndarray, 
    valid_loader: torch.utils.data.DataLoader
) -> pd.Series:
    """検証フェーズ
    与えられたモデル・データローダを使って検証フェーズを実行。スコアの dict と予測した値を返す
    """

    pred = predict(model, valid_loader)

    pd.DataFrame(pred).to_csv('pred.csv')
    score = calculate_metrics(y_valid, pred)


    valid_score = pd.Series(score)
    
    return valid_score.add_prefix("valid_"), pred