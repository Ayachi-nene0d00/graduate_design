import torch
print('CUDA available:', torch.cuda.is_available())
print('CUDA version:', torch.version.cuda if torch.cuda.is_available() else 'N/A')
print('Device count:', torch.cuda.device_count())
if torch.cuda.is_available():
    print('Device name:', torch.cuda.get_device_name(0))
