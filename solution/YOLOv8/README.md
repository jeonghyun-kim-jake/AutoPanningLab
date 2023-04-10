# YOLOv8
- Train and Predict based on [YOLOv8n](https://github.com/ultralytics/ultralytics) (nano)


## Requirements
```shell
$ pip install -t requirements.txt
```

## Test
- Download model with python scripts
```shell
# python download_model.py --t "TARGET_FOLDER"
$ python download_model.py --t 230407
scripts working on  /Volumes/Projects2/protowork/solution/YOLOv8
...
Authentication successful.
[DONE] download  best.pt  at  /Volumes/Projects2/protowork/solution/YOLOv8/230407
[DONE] configs:  {'id': '1M0dF8PIIMipYssgGeu14Iq4v5VvDFXr-', 'link': 'https://drive.google.com/file/d/1M0dF8PIIMipYssgGeu14Iq4v5VvDFXr-/view?usp=share_link'}
```
- run inference by below scripts
```shell
# yolo task=detect mode=predict model=yolov8n.pt conf={confidence} source={image_path} project={project_name} save=True
$ yolo task=detect mode=predict model=230407/best.pt conf=0.25 source="test_images/" project="inference_result" save=True 
```

## Results
| Name             | content                        | etc                     |
|------------------|--------------------------------|-------------------------|
| [230407](230407) | - Epoch 2000<br/> - [yolo8n](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/models/v8/yolov8.yaml) | ![img](230407/results/yolov8_2000epochs_2_jpg.rf.f5061bd2fb923bd35e11b90a2ed404f7.jpg) |

