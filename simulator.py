import os
import sys
import numpy as np
import pandas as pd

class Simulator(object):
    def __init__(self) -> None:
        pass
    
    # 하루 정해서 그날의 수요 / 도착지 / 걸린 시간 가져오고 전처리해서 df로 리턴
    def ReadOrder(input_file_path):
        # read excel file
        df = pd.read_xlsx(input_file_path)
        return df

    # 

