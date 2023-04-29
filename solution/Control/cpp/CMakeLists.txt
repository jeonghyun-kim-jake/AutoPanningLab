cmake_minimum_required(VERSION 3.5)

project(Yolov8CPPInference VERSION 0.1)

set(CMAKE_INCLUDE_CURRENT_DIR ON)
include_directories()

# OpenCV : required version dependency
find_package(OpenCV 4.7.0 REQUIRED)
include_directories(${CMAKE_CURRENT_SOURCE_DIR})
# !OpenCV

set(PROJECT_SOURCES
    main.cpp
    inference.h
    inference.cpp
)

add_executable(Yolov8CPPInference ${PROJECT_SOURCES})
target_link_libraries(Yolov8CPPInference ${OpenCV_LIBS})