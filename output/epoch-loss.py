import re
import matplotlib.pyplot as plt

log_file = "bert-sim.log"  # 日志文件名
epochs = []
losses = []
with open(log_file, "r") as f:
    for line in f:
        match = re.search(r"EPOCH = \[(\d+)/\d+\] global_step = \d+   loss = (\d+\.\d+)", line)
        if match:
            epoch = int(match.group(1))
            loss = float(match.group(2))
            epochs.append(epoch)
            losses.append(loss)

plt.plot(epochs, losses)
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training Loss")
plt.show()
