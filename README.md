## SingTown AI Trainer Yolov5 RockChip

## Support Models

- yolov8n_192
- yolov8n_256
- yolov8n_320
- yolov8n_416

## Test

```
# test
unset SINGTOWN_AI_HOST
unset SINGTOWN_AI_TOKEN
unset SINGTOWN_AI_TASK_ID
export SINGTOWN_AI_MOCK_TASK_PATH="../mock-task.json"
export SINGTOWN_AI_MOCK_DATASET_PATH="../object-detection-20.json"
bash run.sh
```


```
# test
export SINGTOWN_AI_HOST="https://ai.singtown.com"
export SINGTOWN_AI_TOKEN="your token"
export SINGTOWN_AI_TASK_ID="your id"
unset SINGTOWN_AI_MOCK_TASK_PATH
unset SINGTOWN_AI_MOCK_DATASET_PATH
bash run.sh
```
