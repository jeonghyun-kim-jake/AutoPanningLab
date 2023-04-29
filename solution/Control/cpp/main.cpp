#include <iostream>
#include <vector>
#include <getopt.h>
#include <string>

#include <opencv2/opencv.hpp>

#include "inference.h"
#include "Logs.h"

using namespace std;
using namespace cv;

int main(int argc, char **argv)
{
    LOGI("Started to test");
    
    std::string projectBasePath = "/home/pi/Projects/protowork/solution/Control"; // Set your ultralytics base path

    bool runOnGPU = false;

    //
    // Pass in either:
    //
    // "yolov8s.onnx" or "yolov5s.onnx"
    //
    // To run Inference with yolov8/yolov5 (ONNX)
    //

    // Note that in this example the classes are hard-coded and 'classes.txt' is a place holder.
    Inference inf(projectBasePath + "/python/visions/models/best.onnx", cv::Size(640, 640),
                  projectBasePath+"/python/visions/models/classes.txt", runOnGPU);

    std::vector<std::string> imageNames;
    imageNames.push_back(projectBasePath + "/test.jpg");

    for (int i = 0; i < imageNames.size(); ++i)
    {        
        LOGI("Loaded image %s", imageNames[i].c_str());
        cv::Mat frame = cv::imread(imageNames[i]);

        LOGI("Inference started %d", i+1);
        // Inference starts here...
        std::vector<Detection> output = inf.runInference(frame);

        int detections = output.size();
        int ignored = 0;
        LOGI("Number of detections: %d",  detections);

        for (int i = 0; i < detections; ++i)
        {
            Detection detection = output[i];
            
            if(detection.confidence<0.5){
                ignored++;
                continue;
            }

            cv::Rect box = detection.box;
            cv::Scalar color = detection.color;

            // Detection box
            cv::rectangle(frame, box, color, 2);

            // Detection box text
            std::string classString = detection.className + ' ' + std::to_string(detection.confidence).substr(0, 4);
            cv::Size textSize = cv::getTextSize(classString, cv::FONT_HERSHEY_DUPLEX, 1, 2, 0);
            cv::Rect textBox(box.x, box.y - 40, textSize.width + 10, textSize.height + 20);

            cv::rectangle(frame, textBox, color, cv::FILLED);
            cv::putText(frame, classString, cv::Point(box.x + 5, box.y - 10), cv::FONT_HERSHEY_DUPLEX, 1, cv::Scalar(0, 0, 0), 2, 0);
        }
        if(ignored > 0){
            LOGI("Ignored detection by low confidence: %d",  ignored);            
        }
        // Inference ends here...

        // This is only for preview purposes
        float scale = 0.8;
        cv::resize(frame, frame, cv::Size(frame.cols*scale, frame.rows*scale));
        // cv::imshow("Inference", frame);
        if(!cv::imwrite("result"+std::to_string(i)+"_detected"+std::to_string(detections-ignored)+".jpg", frame)){
            LOGE("Failed to write result image")
        }

        cv::waitKey(-1);
    }
    LOGI("Finished to test");
}