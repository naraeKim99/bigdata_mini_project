#1. 이상치 제거함수
titanic=[0] # 데이터
import numpy as np
def outfliers_iqr(data):
    q1,q3=np.percentile(data,[25,75])
    iqr=q3-q1
    lower_bound=q1-(iqr*1.5)
    upper_bound=q3+(iqr*1.5)
    return lower_bound, upper_bound