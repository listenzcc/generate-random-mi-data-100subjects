"""
File: main.py
Author: Chuncheng Zhang
Date: 2025-09-23
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Generate random MI data and save into .mat file.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-09-23 ------------------------
# Requirements and constants
import random
import win32file
import win32con
import pywintypes
import numpy as np
from pathlib import Path
from scipy.io import savemat, loadmat

data_directory = Path("./data")
data_directory.mkdir(parents=True, exist_ok=True)

# %% ---- 2025-09-23 ------------------------
# Function and class


def change_creation_time_windows(path, new_time):
    """
    Windows 系统下修改文件创建时间
    需要安装: pip install pywin32
    """
    # 打开文件句柄
    handle = win32file.CreateFile(
        path.as_posix(),
        win32con.GENERIC_WRITE,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_ATTRIBUTE_NORMAL,
        None
    )

    # 创建 pywintypes 时间对象
    py_time = pywintypes.Time(new_time)

    # 设置文件时间
    win32file.SetFileTime(handle, py_time)

    # 关闭句柄
    handle.close()
    return


def generate_random_mi_data(num_samples, num_channels, num_timepoints, num_classes):
    """
    Generate random MI data.

    Parameters:
        num_samples (int): Number of samples.
        num_channels (int): Number of channels.
        num_timepoints (int): Number of time points.
        num_classes (int): Number of classes.

    Returns:
        X (np.ndarray): Generated data of shape (num_samples, num_channels, num_timepoints).
        y (np.ndarray): Generated labels of shape (num_samples,).
    """
    X = np.random.randn(num_samples, num_channels, num_timepoints)
    y = np.random.randint(0, num_classes, size=(num_samples,))
    return X, y


def generate_random_datetime(y=2025, m=7, d=None):
    """
    Generate random datetime string in the format "YYYY-MM-DD HH:MM:SS".

    Parameters:
        y (int): Year.
        m (int): Month.
        d (int): Day.

    Returns:
        str: Random datetime string.
    """
    if d is None:
        d = random.randint(1, 28)  # To avoid month-end issues

    hour = random.randint(8, 17)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return f"{y}-{m:02d}-{d:02d} {hour:02d}:{minute:02d}:{second:02d}"


# %% ---- 2025-09-23 ------------------------
# Play ground
if __name__ == "__main__":
    # Parameters
    num_samples = 100  # Number of samples
    num_channels = 22  # Number of channels
    num_timepoints = 1000  # Number of time points
    num_classes = 2  # Number of classes
    ch_names = [f'Ch{i+1}' for i in range(num_channels)]

    # Generate random MI data
    X, y = generate_random_mi_data(
        num_samples, num_channels, num_timepoints, num_classes)

    # Subject information
    subject = {
        'id': "S0001",
        'date': generate_random_datetime(2025, 7),
        'ch_names': ch_names,
    }

    # Save to .mat file
    output_path = data_directory.joinpath(f"{subject['id']}.mat")
    savemat(output_path, {'X': X, 'y': y, 'subject': subject})
    print(f"Random MI data saved to {output_path}")

    # Set to 2023-07-23 00:00:00
    # Convert subject['date'] to timestamp
    timestamp = np.datetime64(subject['date']).astype(
        'datetime64[s]').astype(float)
    change_creation_time_windows(output_path, timestamp)

    loaded = loadmat(output_path)
    print(f'Loaded keys: {loaded.keys()}')
    for key in loaded:
        if key.startswith('__'):
            continue
        print(
            f'{key}: {type(loaded[key])}, shape: {loaded[key].shape if isinstance(loaded[key], np.ndarray) else "N/A"}')
    print(loaded['subject'])


# %% ---- 2025-09-23 ------------------------
# Pending


# %% ---- 2025-09-23 ------------------------
# Pending
