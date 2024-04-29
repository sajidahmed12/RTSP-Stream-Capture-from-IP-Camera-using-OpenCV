cmake_minimum_required(VERSION 3.10)
project(RTSPRecorder)

# Set C++ Standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find packages
find_package(OpenCV REQUIRED)
find_package(Boost REQUIRED COMPONENTS system filesystem program_options)

# Include directories
include_directories(${Boost_INCLUDE_DIRS} ${OpenCV_INCLUDE_DIRS})

# Define the executable
add_executable(rtsp_video_downloader rtsp_video_downloader.cpp)

# Link libraries
target_link_libraries(rtsp_video_downloader ${OpenCV_LIBS} ${Boost_LIBRARIES})
