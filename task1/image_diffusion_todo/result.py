import subprocess
import csv
import os

steps_list = [10, 20, 50, 100, 1000]
eta_list = [0.0, 0.2, 0.5, 1.0]
ckpt_path = "./ln.ckpt"
gpu = "0"
eval_data_dir = "data/afhq/eval/"

results = []

for steps in steps_list:
    for eta in eta_list:
        sample_dir = f"samples_ddim_steps{steps}_eta{eta}"
        os.makedirs(sample_dir, exist_ok=True)
        # Step 1: Sampling
        sample_cmd = [
            "python", "sampling.py",
            "--ckpt_path", ckpt_path,
            "--save_dir", sample_dir,
            "--sample_method", "ddim",
            "--ddim_steps", str(steps),
            "--eta", str(eta),
            "--gpu", gpu
        ]
        print("Running:", " ".join(sample_cmd))
        subprocess.run(sample_cmd, check=True)
        # Step 2: FID
        fid_cmd = [
            "python", "fid/measure_fid.py",
            eval_data_dir,
            sample_dir
        ]
        print("Running:", " ".join(fid_cmd))
        result = subprocess.run(fid_cmd, capture_output=True, text=True, check=True)
        # 解析 FID
        fid_value = None
        for line in result.stdout.splitlines():
            if line.startswith("FID:"):
                fid_value = float(line.split(":")[1].strip())
                break
        results.append({"steps": steps, "eta": eta, "fid": fid_value})

# Step 3: 寫入 CSV
with open("ddim_fid_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["steps", "eta", "fid"])
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print("所有組合已完成，結果已存入 ddim_fid_results.csv")