#include <opencv2/opencv.hpp>
#include <boost/program_options.hpp>
#include <boost/filesystem.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>
#include <iostream>
#include <vector>
#include <thread>
#include <chrono>

namespace po = boost::program_options;
namespace fs = boost::filesystem;

void rtsp_record(std::string cam_username, std::string cam_pass, std::string ip, int num, int fps, bool save_video, bool live, std::string start_time, int end_time, std::string out_dir) {
    std::string RTSP_URL;
    if (live) {
        RTSP_URL = "rtsp://" + cam_username + ":" + cam_pass + "@" + ip + "/ISAPI/Streaming/channels/" + std::to_string(num) + "01";
    } else {
        RTSP_URL = "rtsp://" + cam_username + ":" + cam_pass + "@" + ip + "/ISAPI/Streaming/tracks/" + std::to_string(num) + "01?starttime=" + start_time + "Z";
    }

    std::cout << "RTSP URL: " << RTSP_URL << std::endl;

    cv::VideoCapture cap(RTSP_URL, cv::CAP_FFMPEG);
    if (!cap.isOpened()) {
        std::cerr << "Cannot open RTSP stream." << std::endl;
        return;
    }

    int frame_width = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_WIDTH));
    int frame_height = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_HEIGHT));
    std::string to_date = boost::posix_time::to_iso_string(boost::posix_time::second_clock::local_time());
    std::string full_out_dir = fs::path(out_dir).append(to_date).string();
    fs::create_directories(full_out_dir);

    std::string video_filename = to_date + "_cam_" + std::to_string(num) + ".mp4";
    std::string video_filepath = fs::path(full_out_dir).append(video_filename).string();
    cv::VideoWriter video_output(video_filepath, cv::VideoWriter::fourcc('X', 'V', 'I', 'D'), fps, cv::Size(frame_width, frame_height), true);

    std::cout << "[INFO]: RTSP Streaming Started....." << std::endl;
    auto start = std::chrono::system_clock::now();
    int frame_count = 0;

    while (true) {
        cv::Mat frame;
        if (!cap.read(frame)) {
            break;
        }
        frame_count++;
        auto now = std::chrono::system_clock::now();
        auto elapsed_time = std::chrono::duration_cast<std::chrono::seconds>(now - start).count();

        if (save_video && (elapsed_time < end_time * 60)) {
            video_output.write(frame);
            std::cout << "[INFO]: Saving video frame " << frame_count << " at " << fps << " fps....cam " << num << std::endl;
        }

        if (cv::waitKey(1) == 'q' || elapsed_time >= end_time * 60) {
            std::cout << "\n [INFO]: Stopping recording..." << std::endl;
            break;
        }
    }

    cap.release();
    video_output.release();
    std::cout << "All videos saved successfully.!" << std::endl;
}

int main(int argc, char* argv[]) {
    po::options_description desc("Allowed options");
    desc.add_options()
        ("cam_username", po::value<std::string>()->default_value("admin"), "ip_camera's username")
        ("cam_pass", po::value<std::string>()->default_value("admin"), "ip_camera's password")
        ("ip", po::value<std::string>()->default_value("192.168.0.5"), "ip_camera's ip address")
        ("cam_list", po::value<std::vector<int>>()->multitoken()->required(), "Set camera range")
        ("save_video", po::value<bool>()->default_value(true), "Save the RTSP video")
        ("fps", po::value<int>()->default_value(4), "FPS")
        ("live", po::value<bool>()->default_value(false), "Live record or Tracks playback record")
        ("start_time", po::value<std::string>()->default_value("20240423T114200"), "Playback start-time")
        ("end_time", po::value<int>()->default_value(5), "Playback end-time in minutes")
        ("out_dir", po::value<std::string>()->default_value(boost::posix_time::to_iso_string(boost::posix_time::second_clock::local_time())), "Output directory");

    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);

    std::vector<int> cam_list = vm["cam_list"].as<std::vector<int>>();
    std::vector<std::thread> threads;

    for (int i = cam_list[0]; i <= cam_list[1]; ++i) {
        threads.emplace_back(rtsp_record, vm["cam_username"].as<std::string>(), vm["cam_pass"].as<std::string>(), vm["ip"].as<std::string>(), i, vm["fps"].as<int>(), vm["save_video"].as<bool>(), vm["live"].as<bool>(), vm["start_time"].as<std::string>(), vm["end_time"].as<int>(), vm["out_dir"].as<std::string>());
    }

    for (auto& thread : threads) {
        thread.join();
    }

    return 0;
}
