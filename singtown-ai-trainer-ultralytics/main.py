from singtown_ai import SingTownAIClient
from singtown_ai import stdout_watcher, file_watcher, error_watcher
from singtown_ai import export_yolo

client = SingTownAIClient()

@stdout_watcher(interval=1)
def on_stdout_write(content: str):
    client.log(content, end="")

@error_watcher()
def on_error():
    client.failed()

from ultralytics import YOLO
from pathlib import Path
import shutil
from zipfile import ZipFile

DATASET_PATH = Path("../dataset")
RUNS_PATH = Path("../runs").absolute()
shutil.rmtree(RUNS_PATH, ignore_errors=True)
RUNS_PATH.mkdir(parents=True)
METRICS_PATH = RUNS_PATH / "train/results.csv"

@file_watcher(METRICS_PATH, interval=3)
def file_on_change(content: str):
    import csv
    from io import StringIO

    metrics = list(csv.DictReader(StringIO(content)))
    if not metrics:
        return
    client.update_metrics(metrics)

LABELS = client.task.project.labels
MODEL_NAME = client.task.model_name
EPOCHS = client.task.epochs
BATCH_SIZE = client.task.batch_size
LEARNING_RATE = client.task.learning_rate
EXPORT_WIDTH = client.task.export_width
EXPORT_HEIGHT = client.task.export_height

MODEL_CLASS, IMG_SZ = MODEL_NAME.split("_")

print("Download dataset")
export_yolo(client, DATASET_PATH)

model = YOLO("yolov8n.pt")
results = model.train(data="../dataset/data.yaml", epochs=EPOCHS, imgsz=IMG_SZ, batch=BATCH_SIZE, project=str(RUNS_PATH))
print(results)

export_path = model.export(format="tflite", int8=True, data="../dataset/data.yaml", simplify=True, end2end=False, imgsz=(EXPORT_HEIGHT, EXPORT_WIDTH))
export_path = Path(export_path).parent / "best_integer_quant.tflite"
print(f"Exported model to {export_path}")

with open(RUNS_PATH/"trained.txt", "wb") as f:
    f.write("\n".join(LABELS).encode("utf-8"))

with ZipFile(RUNS_PATH/"result.zip", 'w') as zip:
    zip.write("openmv_yolov8n.py", arcname="main.py")
    zip.write(export_path, arcname="trained.tflite")
    zip.write(RUNS_PATH/"trained.txt", arcname="trained.txt")

client.upload_results_zip(RUNS_PATH/"result.zip")
client.success()
print("Finished")
